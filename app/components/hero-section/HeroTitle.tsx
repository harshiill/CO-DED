import { Button, Text, Group } from '@mantine/core';
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

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % texts.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      backgroundColor: '#0F172A',
      display: 'flex',
      justifyContent: 'center',
      alignItems:'center',
      padding: '100px 20px',
      
      minHeight: '100vh',
      width:'100vw'
      
    }}>
      <div style={{ textAlign: 'center', maxWidth: '800px', paddingRight: '20px' }}>
        
        <h1 style={{
          fontSize: '3rem',
          fontWeight: 800,
          marginBottom: '10px',
          color: '#fff',
          fontFamily: 'Merriweather, sans-serif',
        }}>
          Your{' '}
          <span style={{
            background: 'linear-gradient(90deg, #4ADE80 0%, #22D3EE 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            one-stop solution
          </span>{' '}
          to
        </h1>

        <motion.h2
          key={texts[index]}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{
            fontSize: '2.3rem',
            fontWeight: 700,
            color: '#fff',
            marginBottom: '15px',
          }}
        >
          {texts[index]}
        </motion.h2>

        <TextAnimate.Typewriter style={{
          fontSize: '1.6rem',
          lineHeight: '2.2rem',
          color: '#94A3B8',
          padding: '1rem',
          fontFamily: 'Merriweather, sans-serif',
        }} value="Supercharge your website's SEO – analyze, detect broken links, and optimize performance with our cutting-edge tools!" animate />

        <Group style={{ marginTop: '30px', justifyContent: 'center', gap: '15px' }}>
          <Button
            size="lg"
            variant="filled"
            style={{
              backgroundColor: '#4ADE80',
              color: '#0F172A',
              padding: '12px 24px',
              fontSize: '1rem',
              fontWeight: 600,
              borderRadius: '8px',
              transition: 'background-color 0.3s ease',
            }}
          >
            Get Started
          </Button>
        </Group>
      </div>
    </div>
  );
}
