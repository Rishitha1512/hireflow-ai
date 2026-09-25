import { useState } from "react"

const STAGES = [
  { id: "upload", label: "Upload resume" },
  { id: "review", label: "Review candidate" },
  { id: "ask", label: "Ask questions" },
  { id: "evaluate", label: "Generate evaluation" },
  { id: "export", label: "Export report" },
]

function App() {
  const [file, setFile] = useState(null)
  const [candidate, setCandidate] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [asking, setAsking] = useState(false)
  const [evaluation, setEvaluation] = useState(null)
  const [evaluating, setEvaluating] = useState(false)
  const [exporting, setExporting] = useState(false)

  const analyzeResume = async () => {
    if (!file) {
      setError("Choose a PDF resume before analyzing.")
      return
    }

    setLoading(true)
    setError("")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Failed to analyze resume")
      }

      const data = await response.json()
      setCandidate(data.candidate)
      setEvaluation(null)
      setAnswer("")
    } catch {
      setError("The resume couldn't be analyzed. Check the server and try again.")
    } finally {
      setLoading(false)
    }
  }

  const askAI = async () => {
    if (!candidate) {
      setAnswer("Upload and analyze a resume first.")
      return
    }

    if (!question.trim()) {
      setAnswer("Type a question first.")
      return
    }

    setAsking(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, candidate }),
      })

      if (!response.ok) {
        throw new Error("Failed to get AI answer")
      }

      const data = await response.json()
      setAnswer(data.answer)
    } catch {
      setAnswer("That question couldn't be answered. Check the server and try again.")
    } finally {
      setAsking(false)
    }
  }

  const generateEvaluation = async () => {
    if (!candidate) {
      setError("Upload and analyze a resume first.")
      return
    }

    setError("")
    setEvaluating(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ candidate }),
      })

      if (!response.ok) {
        throw new Error("Failed to generate evaluation")
      }

      const data = await response.json()
      setEvaluation(data.evaluation)
    } catch {
      setError("The evaluation couldn't be generated. Check the server and try again.")
    } finally {
      setEvaluating(false)
    }
  }

  const generatePDF = async () => {
    if (!candidate || !evaluation) {
      setError("Generate the evaluation before exporting.")
      return
    }

    setError("")
    setExporting(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/generate-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ candidate, evaluation }),
      })

      if (!response.ok) {
        throw new Error("Failed to generate PDF")
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = url
      link.download = "candidate_evaluation.pdf"
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch {
      setError("The report couldn't be exported. Check the server and try again.")
    } finally {
      setExporting(false)
    }
  }

  const stageStatus = (id) => {
    if (id === "upload") return candidate ? "done" : file ? "active" : "pending"
    if (id === "review") return candidate ? (evaluation ? "done" : "active") : "pending"
    if (id === "ask") return candidate ? (answer ? "done" : "active") : "pending"
    if (id === "evaluate") return evaluation ? "done" : candidate ? "active" : "pending"
    if (id === "export") return evaluation ? "active" : "pending"
    return "pending"
  }

  return (
    <div className="min-h-screen bg-[#0F1115] text-[#ECEDF1] font-sans">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=Inter:wght@400;500;600&display=swap');
        .font-serif-display { font-family: 'Source Serif 4', Georgia, serif; }
        .font-sans { font-family: 'Inter', system-ui, sans-serif; }
      `}</style>

      {/* Header */}
      <header className="border-b border-[#272C36]">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
          <div>
            <h1 className="font-serif-display text-[1.6rem] font-semibold tracking-tight text-[#ECEDF1]">
              HireFlow
            </h1>
            <p className="mt-1 text-[13px] text-[#8B90A0]">
              A reading desk for candidate resumes
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-[#272C36] bg-[#171A21] px-3 py-1.5">
            <span
              className={`h-1.5 w-1.5 rounded-full ${
                candidate ? "bg-[#5FAE82]" : "bg-[#5B606E]"
              }`}
            />
            <span className="text-[12px] text-[#8B90A0]">
              {candidate ? `Reviewing ${candidate.name || "candidate"}` : "No candidate loaded"}
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">
        <div className="grid gap-10 lg:grid-cols-[240px_1fr]">

          {/* Left rail: stepper + candidate snapshot */}
          <aside className="lg:sticky lg:top-10 lg:self-start">
            <ol className="space-y-0">
              {STAGES.map((stage, i) => {
                const status = stageStatus(stage.id)
                return (
                  <li key={stage.id} className="flex gap-3">
                    <div className="flex flex-col items-center">
                      <span
                        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border text-[11px] ${
                          status === "done"
                            ? "border-[#E3A34D] bg-[#E3A34D] text-[#0F1115] font-medium"
                            : status === "active"
                            ? "border-[#E3A34D] text-[#E3A34D]"
                            : "border-[#3A404D] text-[#5B606E]"
                        }`}
                      >
                        {status === "done" ? "✓" : i + 1}
                      </span>
                      {i < STAGES.length - 1 && (
                        <span
                          className={`w-px flex-1 ${
                            status === "done" ? "bg-[#E3A34D]" : "bg-[#272C36]"
                          }`}
                          style={{ minHeight: "28px" }}
                        />
                      )}
                    </div>
                    <p
                      className={`pb-7 pt-0.5 text-[13px] ${
                        status === "pending" ? "text-[#5B606E]" : "text-[#ECEDF1]"
                      }`}
                    >
                      {stage.label}
                    </p>
                  </li>
                )
              })}
            </ol>

            <div className="mt-2 border-t border-[#272C36] pt-6">
              <p className="text-[12px] text-[#5B606E]">Candidate</p>
              <p className="mt-2 font-serif-display text-lg text-[#ECEDF1]">
                {candidate?.name || "—"}
              </p>
              <p className="mt-1 text-[13px] text-[#8B90A0]">
                {candidate?.email || "Not yet analyzed"}
              </p>
              {candidate?.skills?.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {candidate.skills.slice(0, 8).map((skill, i) => (
                    <span
                      key={i}
                      className="rounded-full border border-[#272C36] bg-[#171A21] px-2.5 py-1 text-[11px] text-[#8B90A0]"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </aside>

          {/* Main column */}
          <div className="space-y-6">

            {/* Upload */}
            <section className="rounded-lg border border-[#272C36] bg-[#171A21] p-7">
              <h2 className="font-serif-display text-lg font-semibold text-[#ECEDF1]">
                Resume
              </h2>
              <p className="mt-1.5 text-[13px] leading-relaxed text-[#8B90A0]">
                Upload a PDF and HireFlow will pull out the candidate's name, contact details, and skills.
              </p>

              <label className="mt-5 flex cursor-pointer items-center justify-between rounded-md border border-dashed border-[#3A404D] bg-[#0F1115] px-5 py-4 transition-colors hover:border-[#E3A34D]/60">
                <span className="text-[13px] text-[#8B90A0]">
                  {file ? file.name : "Choose a PDF file"}
                </span>
                <span className="rounded-md border border-[#3A404D] px-3 py-1.5 text-[12px] text-[#ECEDF1]">
                  Browse
                </span>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden"
                />
              </label>

              <div className="mt-5 flex items-center gap-4">
                <button
                  onClick={analyzeResume}
                  disabled={loading}
                  className="rounded-md bg-[#E3A34D] px-5 py-2.5 text-[13px] font-medium text-[#0F1115] transition-colors hover:bg-[#F0B662] disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? "Analyzing…" : "Analyze resume"}
                </button>
                {error && <p className="text-[13px] text-[#E2665B]">{error}</p>}
              </div>
            </section>

            {/* Ask AI */}
            <section className="rounded-lg border border-[#272C36] bg-[#171A21] p-7">
              <h2 className="font-serif-display text-lg font-semibold text-[#ECEDF1]">
                Ask about this candidate
              </h2>
              <p className="mt-1.5 text-[13px] leading-relaxed text-[#8B90A0]">
                Ask a specific question and get an answer grounded in the resume.
              </p>

              <div className="mt-5 flex gap-3">
                <input
                  type="text"
                  placeholder="What skills does the candidate have?"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && askAI()}
                  className="w-full rounded-md border border-[#272C36] bg-[#0F1115] px-4 py-2.5 text-[13px] text-[#ECEDF1] outline-none placeholder:text-[#5B606E] focus:border-[#E3A34D]/60"
                />
                <button
                  onClick={askAI}
                  disabled={asking}
                  className="shrink-0 rounded-md border border-[#3A404D] px-5 py-2.5 text-[13px] font-medium text-[#ECEDF1] transition-colors hover:border-[#E3A34D]/60 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {asking ? "Asking…" : "Ask"}
                </button>
              </div>

              <div className="mt-5 rounded-md border border-[#272C36] bg-[#0F1115] p-4 text-[13px] leading-relaxed text-[#ECEDF1]/90">
                {answer || (
                  <span className="text-[#5B606E]">The answer will appear here.</span>
                )}
              </div>
            </section>

            {/* Evaluation */}
            <section className="rounded-lg border border-[#272C36] bg-[#171A21] p-7">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="font-serif-display text-lg font-semibold text-[#ECEDF1]">
                    Evaluation
                  </h2>
                  <p className="mt-1.5 text-[13px] leading-relaxed text-[#8B90A0]">
                    A structured read of the candidate, built only from the resume.
                  </p>
                </div>
                <button
                  onClick={generateEvaluation}
                  disabled={evaluating}
                  className="shrink-0 rounded-md bg-[#E3A34D] px-5 py-2.5 text-[13px] font-medium text-[#0F1115] transition-colors hover:bg-[#F0B662] disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {evaluating ? "Generating…" : "Generate evaluation"}
                </button>
              </div>

              {evaluation && (
                <div className="mt-6 space-y-5">
                  <div className="grid gap-5 sm:grid-cols-2">
                    <div className="rounded-md border border-[#272C36] bg-[#0F1115] p-5">
                      <p className="text-[12px] text-[#5B606E]">Experience</p>
                      <p className="mt-2 text-[13px] leading-relaxed text-[#ECEDF1]">
                        {evaluation.experience_summary || "Not available"}
                      </p>
                    </div>
                    <div className="rounded-md border border-[#272C36] bg-[#0F1115] p-5">
                      <p className="text-[12px] text-[#5B606E]">Strengths</p>
                      <ul className="mt-2 space-y-1.5">
                        {evaluation.strengths?.map((strength, i) => (
                          <li
                            key={i}
                            className="flex gap-2 text-[13px] leading-relaxed text-[#ECEDF1]"
                          >
                            <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-[#5FAE82]" />
                            {strength}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {evaluation.missing_information?.length > 0 && (
                    <div className="rounded-md border border-[#272C36] bg-[#0F1115] p-5">
                      <p className="text-[12px] text-[#5B606E]">Missing information</p>
                      <ul className="mt-2 space-y-1.5">
                        {evaluation.missing_information.map((item, i) => (
                          <li
                            key={i}
                            className="flex gap-2 text-[13px] leading-relaxed text-[#ECEDF1]"
                          >
                            <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-[#E2665B]" />
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="rounded-md border-l-2 border-[#E3A34D] bg-[#0F1115] p-5">
                    <p className="text-[12px] text-[#5B606E]">Overall</p>
                    <p className="mt-2 text-[13px] leading-relaxed text-[#ECEDF1]">
                      {evaluation.overall_summary}
                    </p>
                  </div>

                  <div className="flex justify-end border-t border-[#272C36] pt-5">
                    <button
                      onClick={generatePDF}
                      disabled={exporting}
                      className="rounded-md border border-[#3A404D] px-5 py-2.5 text-[13px] font-medium text-[#ECEDF1] transition-colors hover:border-[#E3A34D]/60 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {exporting ? "Preparing…" : "Download PDF report"}
                    </button>
                  </div>
                </div>
              )}
            </section>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App