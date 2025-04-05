"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export default function Form() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    url: "",
    srcDirectory: "",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
  
    if (!formData.username || !formData.password || !formData.url || !formData.srcDirectory) {
      alert("All fields are required!")
      return
    }
  
    try {
      const response = await fetch("http://localhost:8000/api/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
  
      if (!response.ok) {
        throw new Error("Failed to submit form")
      }
  
      const data = await response.json()
      console.log("Form submitted successfully:", data)
      alert("Configuration saved successfully!")
  
      // Optionally, reset form after successful submission
      setFormData({
        username: "",
        password: "",
        url: "",
        srcDirectory: "",
      })
    } catch (error) {
      console.error("Error submitting form:", error)
      alert("Failed to save configuration. Please try again.")
    }
  }
  
  return (
    <Card className="w-full border-0 shadow-none bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <CardHeader className="px-0 pt-0">
        <CardTitle>Configuration Form</CardTitle>
        <CardDescription>Enter your credentials and configuration details</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4 px-0">
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              name="username"
              placeholder="Enter your username"
              value={formData.username}
              onChange={handleChange}
              required
              className="bg-gray-100 dark:bg-gray-800"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
              className="bg-gray-100 dark:bg-gray-800"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="url">URL</Label>
            <Input
              id="url"
              name="url"
              type="url"
              placeholder="https://example.com"
              value={formData.url}
              onChange={handleChange}
              required
              className="bg-gray-100 dark:bg-gray-800"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="srcDirectory">Src Directory</Label>
            <Input
              id="srcDirectory"
              name="srcDirectory"
              placeholder="/path/to/directory"
              value={formData.srcDirectory}
              onChange={handleChange}
              required
              className="bg-gray-100 dark:bg-gray-800"
            />
          </div>
        </CardContent>

        <CardFooter className="px-0 pb-0">
          <Button type="submit" className="w-full bg-blue-500 dark:bg-blue-700 hover:bg-blue-600 dark:hover:bg-blue-800">
            Submit
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}
