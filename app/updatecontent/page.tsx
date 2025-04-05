'use client';

import { useState, useEffect } from 'react';
import { Container, Paper, Text, Title } from '@mantine/core';
import { updateContent } from '../utils/api';
import { useAnalysis } from '../contexts/Analysiscontext';

export default function UpdateContentPage() {
  const { url, analysisData } = useAnalysis();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Typewriter effect states and messages
  const messages = [
    'OOur AI is thinking...',
    'PPlease wait...',
    'Analyzing your content...',
    'Crunching data...',
    'Almost there...',
    'Processing your request...',
    'Generating insights...',
    'Scanning for patterns...',
    'Refining the output...',
    'Loading smart responses...',
    'Examining possibilities...',
    'Calculating probabilities...',
    'Formulating a response...',
    'Digging into data...',
    'Validating information...',
    'Searching for accuracy...',
    'Compiling relevant details...',
    'Assessing the best outcome...',
    'Interpreting your input...',
    'Making sense of the data...',
    'Understanding the context...'
  ];
  const [messageIndex, setMessageIndex] = useState(0);
  const [typedText, setTypedText] = useState('');

  // Cycle through messages every 5 seconds while loading
  useEffect(() => {
    let cycleInterval;
    if (loading) {
      cycleInterval = setInterval(() => {
        setMessageIndex((prev) => (prev + 1) % messages.length);
      }, 5000);
    } else {
      setMessageIndex(0);
    }
    return () => {
      if (cycleInterval) clearInterval(cycleInterval);
    };
  }, [loading]);

  // Typewriter effect for the current message
  useEffect(() => {
    if (loading) {
      const fullMessage = messages[messageIndex];
      setTypedText(''); // Reset the displayed text
      let charIndex = 0;
      const typingInterval = setInterval(() => {
        setTypedText((prev) => prev + fullMessage.charAt(charIndex));
        charIndex++;
        if (charIndex === fullMessage.length) {
          clearInterval(typingInterval);
        }
      }, 100);
      return () => clearInterval(typingInterval);
    }
  }, [messageIndex, loading]);

  useEffect(() => {
    if (url && analysisData?.update) {
      setLoading(true);
      const filteredData = Array.isArray(analysisData.update) ? analysisData.update : [];
      setData(filteredData);
      setLoading(false);
    }
  }, [url, analysisData.update]);
  

  if (!url) {
    return (
      <Container size="md" pt={40}>
        <Title order={2} align="center">
          Please run analysis first from the Dashboard.
        </Title>
      </Container>
    );
  }

  // Filter to only those update objects where analysis.outdated is true
  const outdatedReports = data.filter(
    (report) => report.analysis && report.analysis.outdated
  );

  return (
    <Container size="md" pt={40}>
      <Title
        order={1}
        align="center"
        style={{ fontSize: '4rem', fontWeight: 700 }}
      >
        <span style={{ color: 'lightskyblue' }}>Content Update</span> Suggestor
      </Title>
      {loading && (
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
            width: '100%',
            padding: '20px',
            minHeight: '200px'
          }}
        >
          {/* Terminal header mimicking typical terminal window buttons */}
          <div
            style={{
              padding: '10px 20px',
              borderBottom: '1px solid #333',
              display: 'flex',
              gap: '8px',
              alignItems: 'center'
            }}
          >
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#ff5f56' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#ffbd2e' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#27c93f' }}></div>
            <Text ml="auto" style={{ fontSize: '0.8rem' }}>Terminal</Text>
          </div>
          <div style={{ padding: '20px', whiteSpace: 'pre-wrap' }}>
            {typedText}
          </div>
        </Paper>
      )}
      {!loading && outdatedReports.length > 0 && (
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
            width: '100%',
            padding: '20px',
            minHeight: '200px'
          }}
        >
          {/* Terminal header mimicking typical terminal window buttons */}
          <div
            style={{
              padding: '10px 20px',
              borderBottom: '1px solid #333',
              display: 'flex',
              gap: '8px',
              alignItems: 'center'
            }}
          >
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#ff5f56' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#ffbd2e' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#27c93f' }}></div>
            <Text ml="auto" style={{ fontSize: '0.8rem' }}>Terminal</Text>
          </div>
          <div style={{ padding: '20px', whiteSpace: 'pre-wrap' }}>
            {outdatedReports.map((report, index) => (
              <div key={report.id || index} style={{ marginBottom: '1em' }}>
                <div style={{ color: '#d4d4d4' }}>
                  Report {index + 1}
                </div>
                <div style={{ color: '#888' }}>
                  ─────────────────────────────
                </div>
                <div>
                  <span style={{ color: '#d4d4d4' }}>ID: </span>
                  <span style={{ color: '#f8f8f2' }}>{report.id}</span>
                </div>
                <div>
                  <span style={{ color: '#ff79c6' }}>Reason: </span>
                  <span style={{ color: '#8be9fd' }}>{report.analysis.reason}</span>
                </div>
                {report.analysis.suggestion && (
                  <div>
                    <span style={{ color: '#50fa7b' }}>Suggestion: </span>
                    <span style={{ color: '#f1fa8c' }}>{report.analysis.suggestion}</span>
                  </div>
                )}
                <div style={{ fontSize: '0.8em', marginLeft: '20px', marginTop: '4px' }}>
                  <details style={{ cursor: 'pointer' }}>
                    <summary style={{ color: '#bd93f9' }}>Original Content</summary>
                    <div style={{ color: '#6272a4', marginTop: '4px' }}>
                      {report.orignal_content}
                    </div>
                  </details>
                </div>
                <div style={{ color: '#888', marginTop: '8px' }}>
                  {'─'.repeat(50)}
                </div>
              </div>
            ))}
          </div>
        </Paper>
      )}
      {!loading && outdatedReports.length === 0 && (
        <Text align="center" color="gray" mt={20}>
          {url ? 'No outdated content found.' : 'Please enter a URL to start.'}
        </Text>
      )}
    </Container>
  );
}
