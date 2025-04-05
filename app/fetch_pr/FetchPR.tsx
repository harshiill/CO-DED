import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Github } from "lucide-react";

export default function Home() {
  const githubPrUrl = "https://github.com/yourusername/yourrepository/compare";

  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "1rem",
        backgroundColor: "#F9FAFB",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "400px",
          padding: "2rem",
          backgroundColor: "#fff",
          borderRadius: "8px",
          boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        }}
      >
        <h1
          style={{
            fontSize: "1.8rem",
            fontWeight: "bold",
            textAlign: "center",
            marginBottom: "1rem",
          }}
        >
          GitHub PR Creator
        </h1>
        <p
          style={{
            color: "#6B7280",
            textAlign: "center",
            marginBottom: "1.5rem",
          }}
        >
          Click the button below to create a new Pull Request
        </p>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Link href={githubPrUrl} target="_blank" rel="noopener noreferrer">
            <Button
              size="lg"
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                backgroundColor: "#0F172A",
                color: "#fff",
                padding: "12px 24px",
                borderRadius: "6px",
                fontSize: "1rem",
                fontWeight: "600",
                cursor: "pointer",
                transition: "background-color 0.3s ease",
              }}
              onMouseOver={(e) =>
                (e.currentTarget.style.backgroundColor = "#1E293B")
              }
              onMouseOut={(e) =>
                (e.currentTarget.style.backgroundColor = "#0F172A")
              }
            >
              <Github style={{ width: "20px", height: "20px" }} />
              Need a PR
            </Button>
          </Link>
        </div>
      </div>
    </main>
  );
}
