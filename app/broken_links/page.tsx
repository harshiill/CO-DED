"use client";

import { useState, useEffect } from "react";
import { Container, Paper, Text, Title } from "@mantine/core";
import { getErrorLinks } from "../utils/api";
import { useAnalysis } from "../contexts/Analysiscontext";

export default function BrokenLinksPage() {
  const { url, analysisData } = useAnalysis();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Typewriter effect states and messages
  const messages = [
    "Scanning for broken links...",
    "Checking link integrity...",
    "Analyzing webpage structure...",
    "Validating hyperlinks...",
    "Detecting inaccessible URLs...",
    "Identifying dead links...",
    "Processing your request...",
  ];
  const [messageIndex, setMessageIndex] = useState(0);
  const [typedText, setTypedText] = useState("");

  useEffect(() => {
    let cycleInterval;
    if (loading) {
      cycleInterval = setInterval(() => {
        setMessageIndex((prev) => (prev + 1) % messages.length);
      }, 5000);
    } else {
      setMessageIndex(0);
    }
    return () => cycleInterval && clearInterval(cycleInterval);
  }, [loading]);

  useEffect(() => {
    if (loading) {
      const fullMessage = messages[messageIndex];
      setTypedText("");
      let charIndex = 0;
      const typingInterval = setInterval(() => {
        setTypedText((prev) => prev + fullMessage.charAt(charIndex));
        charIndex++;
        if (charIndex === fullMessage.length) clearInterval(typingInterval);
      }, 100);
      return () => clearInterval(typingInterval);
    }
  }, [messageIndex, loading]);

  useEffect(() => {
    if (url && analysisData?.errorLinks) {
      setLoading(true);
      console.log("Fetched broken links:", analysisData.errorLinks);
      setData(
        Array.isArray(analysisData.errorLinks) ? analysisData.errorLinks : []
      );
      setLoading(false);
    }
  }, [url, analysisData?.errorLinks]);

  if (!url) {
    return (
      <Container size="md" pt={40}>
        <Title order={2} align="center">
          Please run analysis first from the Dashboard.
        </Title>
      </Container>
    );
  }

  const brokenLinks = data.filter((link) => link.status === "broken");

  return (
    <Container size="md" pt={40}>
      <Title
        order={1}
        align="center"
        style={{ fontSize: "4rem", fontWeight: 700 }}
      >
        <span style={{ color: "lightskyblue" }}>Broken Links</span> Detector
      </Title>
      {loading && (
        <Paper
          p="xl"
          shadow="lg"
          withBorder
          mt={40}
          style={{
            backgroundColor: "#1e1e1e",
            color: "#d4d4d4",
            fontFamily: "monospace",
            borderRadius: "8px",
            padding: "20px",
            minHeight: "200px",
          }}
        >
          <div
            style={{
              padding: "10px 20px",
              borderBottom: "1px solid #333",
              display: "flex",
              gap: "8px",
              alignItems: "center",
            }}
          >
            <div
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "50%",
                backgroundColor: "#ff5f56",
              }}
            ></div>
            <div
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "50%",
                backgroundColor: "#ffbd2e",
              }}
            ></div>
            <div
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "50%",
                backgroundColor: "#27c93f",
              }}
            ></div>
            <Text ml="auto" style={{ fontSize: "0.8rem" }}>
              Terminal
            </Text>
          </div>
          <div style={{ padding: "20px", whiteSpace: "pre-wrap" }}>
            {typedText}
          </div>
        </Paper>
      )}
      {!loading && brokenLinks.length > 0 && (
        <Paper
          p="xl"
          shadow="lg"
          withBorder
          mt={40}
          style={{
            backgroundColor: "#1e1e1e",
            color: "#d4d4d4",
            fontFamily: "monospace",
            borderRadius: "8px",
            padding: "20px",
            minHeight: "200px",
          }}
        >
          {brokenLinks.map((link, index) => (
            <div key={index} style={{ marginBottom: "1em" }}>
              <div style={{ color: "#d4d4d4" }}>Link {index + 1}</div>
              <div style={{ color: "#888" }}>─────────────────────────────</div>
              <div>
                <span style={{ color: "#ff79c6" }}>URL: </span>
                <span style={{ color: "#8be9fd" }}>{link.url}</span>
              </div>
              <div>
                <span style={{ color: "#50fa7b" }}>Status: </span>
                <span style={{ color: "#f1fa8c" }}>{link.status}</span>
              </div>
            </div>
          ))}
        </Paper>
      )}
      {!loading && brokenLinks.length === 0 && (
        <Text align="center" color="gray" mt={20}>
          No broken links found.
        </Text>
      )}
    </Container>
  );
}
