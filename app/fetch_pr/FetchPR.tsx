import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Github } from "lucide-react"

export default function Home() {
  // Replace this URL with your actual GitHub repository URL
  const githubPrUrl = "https://github.com/yourusername/yourrepository/compare"

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center">GitHub PR Creator</h1>
        <p className="text-gray-500 text-center">Click the button below to create a new Pull Request</p>
        <div className="flex justify-center">
          <Link href={githubPrUrl} target="_blank" rel="noopener noreferrer">
            <Button size="lg" className="gap-2">
              <Github className="h-5 w-5" />
              Need a PR
            </Button>
          </Link>
        </div>
      </div>
    </main>
  )
}

