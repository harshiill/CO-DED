'use client';

import React from 'react';
import { HeroTitle } from './components/hero-section/HeroTitle';
import { motion } from 'framer-motion';

const HomePage: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      style={{
        height: '100vh',
        width: '100vw',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-start',
        paddingLeft: '10vw', // Keeps content left-aligned
        backgroundColor: '#000', // Pure black background
        color: 'white',
        margin: 0,
        padding: 0,
        overflow: 'hidden', // Ensures no scroll issues
      }}
    >
      <HeroTitle />
    </motion.div>
  );
};

export default HomePage;
