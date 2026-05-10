import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export function ParallaxBackground() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 20;
      const y = (e.clientY / window.innerHeight - 0.5) * 20;
      setMousePosition({ x, y });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
      {/* Layer 1 - Outer glow */}
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
        style={{
          width: '80vw',
          height: '80vw',
          background: 'radial-gradient(circle, rgba(184, 157, 110, 0.25) 0%, transparent 70%)',
        }}
        animate={{
          x: mousePosition.x * 0.5,
          y: mousePosition.y * 0.5,
        }}
        transition={{ type: 'spring', stiffness: 50, damping: 30 }}
      />
      
      {/* Layer 2 - Middle glow */}
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
        style={{
          width: '60vw',
          height: '60vw',
          background: 'radial-gradient(circle, rgba(184, 157, 110, 0.2) 0%, transparent 60%)',
        }}
        animate={{
          x: mousePosition.x * 0.8,
          y: mousePosition.y * 0.8,
        }}
        transition={{ type: 'spring', stiffness: 60, damping: 25 }}
      />
      
      {/* Layer 3 - Inner glow */}
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
        style={{
          width: '40vw',
          height: '40vw',
          background: 'radial-gradient(circle, rgba(184, 157, 110, 0.15) 0%, transparent 50%)',
        }}
        animate={{
          x: mousePosition.x * 1.2,
          y: mousePosition.y * 1.2,
        }}
        transition={{ type: 'spring', stiffness: 70, damping: 20 }}
      />
    </div>
  );
}
