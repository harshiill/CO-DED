'use client';

import { useState, useEffect } from 'react';
import { TextInput, Button, Container, Paper, Text, Stack, Card, Title } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { addContent } from '../utils/api';
import { useAnalysis } from '../contexts/Analysiscontext';

export default function AddContentPage() {
  const { url, analysisData  } = useAnalysis();
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(false);

  const messages = [
    'OOur AI is thinking...', 'PPlease wait...', 'Analyzing your content...',
    'Crunching data...', 'Almost there...', 'Processing your request...',
    'Generating insights...', 'Scanning for patterns...', 'Refining the output...',
    'Loading smart responses...', 'Examining possibilities...', 'Calculating probabilities...',
    'Formulating a response...', 'Digging into data...', 'Validating information...',
    'Searching for accuracy...', 'Compiling relevant details...', 'Assessing the best outcome...',
    'Interpreting your input...', 'Making sense of the data...', 'Understanding the context...'
  ];

  const [messageIndex, setMessageIndex] = useState(0);
  const [typedText, setTypedText] = useState('');

  useEffect(() => {
    let cycleInterval;
    if (loading) {
      cycleInterval = setInterval(() => {
        setMessageIndex((prev) => (prev + 1) % messages.length);
      }, 5000);
    } else {
      setMessageIndex(0);
    }
    return () => clearInterval(cycleInterval);
  }, [loading]);

  useEffect(() => {
    if (loading) {
      const fullMessage = messages[messageIndex];
      setTypedText('');
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
    if (url) {
      setLoading(true);
      const thatData = analysisData.add;
      const filtered = Array.isArray(thatData) ? thatData.filter((item) => item.analysis) : [];
      setContent(filtered);
      setLoading(false);
    }
  }, [url, analysisData]);

  if (!url) {
    return (
      <Container size="md" pt={40}>
        <Title order={2} align="center">
          Please run analysis first from the Dashboard.
        </Title>
      </Container>
    );
  }

  return (
    <Container size="md" pt={40}>
      <Title
        order={1}
        align="center"
        style={{ fontSize: '4rem', fontWeight: 700 }}
      >
        <span style={{ color: 'lightskyblue' }}>New Content</span> Suggestor
      </Title>
      {loading ? (
        <Paper
          p="xl"
          shadow="lg"
          withBorder
          mt={40}
          style={{
            backgroundColor: '#1e1e1e',
            color: '#d4d4d4',
            fontFamily: 'monospace',
            borderRadius: '8px',
            minHeight: '200px'
          }}
        >
          <div style={{ padding: '20px', whiteSpace: 'pre-wrap' }}>{typedText}</div>
        </Paper>
      ) : content.length > 0 ? (
        <Paper
          p="xl"
          shadow="lg"
          withBorder
          mt={40}
          style={{
            backgroundColor: '#1e1e1e',
            color: '#d4d4d4',
            fontFamily: 'monospace',
            borderRadius: '8px',
            minHeight: '200px'
          }}
        >
          {content.map((report, index) => (
            <div key={report.id || index} style={{ marginBottom: '1em' }}>
              <div style={{ color: '#d4d4d4' }}>Report {index + 1}</div>
              <div>
                <span style={{ color: '#d4d4d4' }}>ID: </span>
                <span style={{ color: '#f8f8f2' }}>{report.id}</span>
              </div>
              <div>
                <span style={{ color: '#ff79c6' }}>Reason: </span>
                <span style={{ color: '#8be9fd' }}>{report.analysis?.reason}</span>
              </div>
            </div>
          ))}
        </Paper>
      ) : (
        <Text align="center" color="gray" mt={20}>
          No content found.
        </Text>
      )}
    </Container>
  );
}
