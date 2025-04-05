import { useState, useEffect } from 'react';
import { TextAnimate } from '@gfazioli/mantine-text-animate';

const typewriterMessages = [
  "Supercharge your website's SEO!",
  "Analyze & Detect Broken Links.",
  "Boost your site's performance.",
  "Audit content & fix issues fast.",
  "Optimize like a pro effortlessly.",
];

export function HeroTypewriter() {
  const [currentMessage, setCurrentMessage] = useState(typewriterMessages[0]);

  useEffect(() => {
    let lastIndex = 0;
    const interval = setInterval(() => {
      let newIndex;
      do {
        newIndex = Math.floor(Math.random() * typewriterMessages.length);
      } while (newIndex === lastIndex);  // ensures no repeat immediately

      lastIndex = newIndex;
      setCurrentMessage(typewriterMessages[newIndex]);
    }, 4000); // change message every 4 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <TextAnimate.Typewriter
      style={{
        fontSize: '1.6rem',
        lineHeight: '2.2rem',
        padding: '1rem',
        fontFamily: 'Merriweather, sans-serif',
      }}
      value={currentMessage}
      animate
    />
  );
}
