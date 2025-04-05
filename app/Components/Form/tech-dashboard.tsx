"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import Form from "./form";

// Technology data with logos and names
const technologies = [
  {
    id: "mongodb",
    name: "MongoDB",
    logo: "https://upload.wikimedia.org/wikipedia/commons/9/93/MongoDB_Logo.svg",
    color: "bg-green-100 hover:bg-green-200 dark:bg-green-900 dark:hover:bg-green-800",
    borderColor: "border-green-300 dark:border-green-600",
    textColor: "text-gray-800 dark:text-gray-100",
  },
  {
    id: "nextjs",
    name: "Next.js",
    logo: "https://upload.wikimedia.org/wikipedia/commons/8/8e/Nextjs-logo.svg",
    color: "bg-black hover:bg-gray-800 dark:bg-gray-900 dark:hover:bg-gray-700",
    borderColor: "border-gray-600 dark:border-gray-500",
    textColor: "text-white",
  },
  {
    id: "react",
    name: "React",
    logo: "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg",
    color: "bg-blue-100 hover:bg-blue-200 dark:bg-blue-900 dark:hover:bg-blue-800",
    borderColor: "border-blue-300 dark:border-blue-600",
    textColor: "text-gray-800 dark:text-gray-100",
  },
  {
    id: "tailwind",
    name: "Tailwind CSS",
    logo: "https://upload.wikimedia.org/wikipedia/commons/d/d5/Tailwind_CSS_Logo.svg",
    color: "bg-cyan-100 hover:bg-cyan-200 dark:bg-cyan-900 dark:hover:bg-cyan-800",
    borderColor: "border-cyan-300 dark:border-cyan-600",
    textColor: "text-gray-800 dark:text-gray-100",
  },
  {
    id: "typescript",
    name: "TypeScript",
    logo: "https://upload.wikimedia.org/wikipedia/commons/4/4c/Typescript_logo_2020.svg",
    color: "bg-blue-100 hover:bg-blue-200 dark:bg-blue-900 dark:hover:bg-blue-800",
    borderColor: "border-blue-300 dark:border-blue-600",
    textColor: "text-gray-800 dark:text-gray-100",
  },
  {
    id: "nodejs",
    name: "Node.js",
    logo: "https://upload.wikimedia.org/wikipedia/commons/d/d9/Node.js_logo.svg",
    color: "bg-green-100 hover:bg-green-200 dark:bg-green-900 dark:hover:bg-green-800",
    borderColor: "border-green-300 dark:border-green-600",
    textColor: "text-gray-800 dark:text-gray-100",
  },
];

export default function TechDashboard() {
  const [selectedTech, setSelectedTech] = useState<string | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);

  const handleTechClick = (techId: string) => {
    setSelectedTech(techId);
    setIsFormOpen(true);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-12 text-gray-900 dark:text-gray-100">
          Select a Technology
        </h1>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6">
          {technologies.map((tech) => (
            <Dialog key={tech.id} open={isFormOpen && selectedTech === tech.id} onOpenChange={setIsFormOpen}>
              <DialogTrigger asChild>
                <button
                  className={`flex flex-col items-center justify-center p-6 rounded-lg border-2 ${tech.color} ${tech.borderColor} ${tech.textColor} transition-all duration-200 transform hover:scale-105`}
                  onClick={() => handleTechClick(tech.id)}
                >
                  <img src={tech.logo} alt={`${tech.name} logo`} className="w-20 h-20 mb-4" />
                  <span className="text-lg font-medium">{tech.name}</span>
                </button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
                <Form />
              </DialogContent>
            </Dialog>
          ))}
        </div>
      </div>
    </div>
  );
}
