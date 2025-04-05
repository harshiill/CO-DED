'use client';
import { useState, useEffect } from 'react';
import { Container, Card, TextInput, Button, Stack, Title, Text, Paper, Loader, Center } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { useAnalysis } from '../contexts/Analysiscontext';
import { useRouter } from 'next/navigation';
import { updateContent, addContent, getErrorLinks, analyzeSEO, setupAider } from '../utils/api';

export default function Dashboard() {
  const [urlInput, setUrlInput] = useState('');
  const [workingDir, setWorkingDir] = useState('');
  const [loading, setLoading] = useState(false);
  const [setupResult, setSetupResult] = useState(null);
  const { setUrl, setAnalysisData } = useAnalysis();
  const router = useRouter();

  const messages = [
    'OOur AI is thinking...',
    'PPlease wait...',
    'AAnalyzing your content...',
    'CCrunching data...',
    'AAlmost there...',
    'PProcessing your request...',
    'GGenerating insights...',
    'SScanning for patterns...',
    'RRefining the output...',
    'LLoading smart responses...',
    'EExamining possibilities...',
    'CCalculating probabilities...',
    'FFormulating a response...',
    'DDigging into data...',
    'VValidating information...',
    'SSearching for accuracy...',
    'CCompiling relevant details...',
    'AAssessing the best outcome...',
    'IInterpreting your input...',
    'MMaking sense of the data...',
    'UUnderstanding the context...'
  ];
  const [messageIndex, setMessageIndex] = useState(0);
  const [typedText, setTypedText] = useState('');

  useEffect(() => {
    let cycle;
    if (loading) {
      cycle = setInterval(() => {
        setMessageIndex((prev) => (prev + 1) % messages.length);
      }, 4000);
    }
    return () => clearInterval(cycle);
  }, [loading]);

  useEffect(() => {
    if (loading) {
      const msg = messages[messageIndex];
      setTypedText('');
      let i = 0;
      const typer = setInterval(() => {
        setTypedText((prev) => prev + msg.charAt(i));
        i++;
        if (i === msg.length) clearInterval(typer);
      }, 80);
      return () => clearInterval(typer);
    }
  }, [messageIndex, loading]);

  const handleSubmit = async () => {
    if (!urlInput || !workingDir) return;
    setLoading(true);
    setUrl(urlInput.trim());

    try {
      const aiderRes = await setupAider(workingDir);
      setSetupResult(aiderRes.stdout || aiderRes.error);

      const [updateRes, addRes, errorRes, seoRes] = await Promise.all([
        updateContent(urlInput.trim()),
        addContent(urlInput.trim()),
        getErrorLinks(urlInput.trim()),
        analyzeSEO(urlInput.trim())
      ]);

      setAnalysisData({
        update: updateRes,
        add: addRes,
        errorLinks: errorRes,
        seo: seoRes,
        workingDir,
      });

      router.push('/updatecontent');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0F172A', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <Container size="sm">
        <Title align="center" style={{ fontSize: '3rem', fontWeight: 800, color: '#fff' }}>
          Dashboard
        </Title>
        <Text align="center" color="dimmed" mb="lg">
          Enter a website URL & your project working directory to analyze.
        </Text>

        <Card shadow="xl" padding="xl" radius="lg" style={{ backgroundColor: '#1E293B', color: '#fff' }}>
          <Stack gap="lg">
            <TextInput
              placeholder="Enter Website URL"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              radius="md"
              size="md"
              rightSection={<IconSearch size={16} />}
            />
            <TextInput
              placeholder="Enter Working Directory"
              value={workingDir}
              onChange={(e) => setWorkingDir(e.target.value)}
              radius="md"
              size="md"
            />
            <Button fullWidth radius="md" size="md" onClick={handleSubmit}>
              Start Analysis
            </Button>
          </Stack>
        </Card>

        {loading && (
          <Paper mt="xl" p="lg" radius="md" style={{ backgroundColor: '#1E293B', color: '#cbd5e1' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <Text size="sm" color="dimmed">
                Terminal
              </Text>
              <Loader size="xs" color="blue" />
            </div>
            <Text style={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>{typedText}</Text>
          </Paper>
        )}

        {setupResult && !loading && (
          <Paper mt="xl" p="lg" radius="md" style={{ backgroundColor: '#1E293B', color: '#cbd5e1' }}>
            <Text style={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>{setupResult}</Text>
          </Paper>
        )}
      </Container>
    </div>
  );
}
