import { Button, Text, Group, useMantineTheme, useComputedColorScheme, Container, Title } from '@mantine/core';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { TextAnimate } from '@gfazioli/mantine-text-animate';

const texts = [
  'Check Broken Links',
  'Analyze SEO',
  'Detect Old Content',
  'Improve Website Performance',
];

export function HeroTitle() {
  const [index, setIndex] = useState(0);
  const theme = useMantineTheme();
  const colorScheme = useComputedColorScheme(); // 'light' or 'dark'

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % texts.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        backgroundColor: colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[0],
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '100px 20px',
        minHeight: '100vh',
        width: '100vw',
      }}
    >
      <Container ta="center" size="lg" px="md">
        <Title
          order={1}
          fw={800}
          mb="xs"
          c={colorScheme === 'dark' ? 'white' : 'dark'}
          style={{ fontFamily: 'Merriweather, sans-serif' }}
        >
          Your{' '}
          <span
            style={{
              background: 'linear-gradient(90deg, #4ADE80 0%, #22D3EE 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            one-stop solution
          </span>{' '}
          to
        </Title>

        <motion.h2
          key={texts[index]}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{
            fontSize: '2.3rem',
            fontWeight: 700,
            color: colorScheme === 'dark' ? theme.white : theme.black,
            marginBottom: '15px',
          }}
        >
          {texts[index]}
        </motion.h2>

        <TextAnimate.Typewriter
          style={{
            fontSize: '1.6rem',
            lineHeight: '2.2rem',
            color: colorScheme === 'dark' ? theme.colors.gray[4] : theme.colors.gray[7],
            padding: '1rem',
            fontFamily: 'Merriweather, sans-serif',
          }}
          value="Supercharge your website's SEO – analyze, detect broken links, and optimize performance with our cutting-edge tools!"
          animate
        />

        <Group mt="xl" justify="center">
          <Button
            size="lg"
            variant="filled"
            color="green"
            radius="md"
          >
            Get Started
          </Button>
        </Group>
      </Container>
    </div>
  );
}
