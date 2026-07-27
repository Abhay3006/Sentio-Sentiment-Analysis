import { PenLine, FileSpreadsheet } from "lucide-react";
import "./ModeToggle.css";

function ModeToggle({ mode, setMode, disabled }) {
  return (
    <div className="mode-toggle" role="tablist">
      <button
        role="tab"
        className={mode === "review" ? "active" : ""}
        disabled={disabled}
        onClick={() => setMode("review")}
      >
        <PenLine />
        Single Review
      </button>
      <button
        role="tab"
        className={mode === "csv" ? "active" : ""}
        disabled={disabled}
        onClick={() => setMode("csv")}
      >
        <FileSpreadsheet />
        Bulk CSV
      </button>
    </div>
  );
}

export default ModeToggle;
