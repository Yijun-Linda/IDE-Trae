import React from 'react';
import { motion } from 'framer-motion';
import { Value } from './concept-diagram-schema';
import { valueExpandAnimation } from './animations';

interface ValueTagProps {
  value: Value;
  isHovered: boolean;
  onHover: (isHovered: boolean) => void;
  index: number;
}

export function ValueTag({ value, isHovered, onHover, index }: ValueTagProps) {
  return (
    <motion.div
      className="relative flex-1 min-w-[200px] max-w-[300px]"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.6,
        delay: 0.8 + index * 0.15,
        ease: [0.16, 1, 0.3, 1]
      }}
      onMouseEnter={() => onHover(true)}
      onMouseLeave={() => onHover(false)}
    >
      <motion.div
        className="p-4 rounded-xl border border-[#e8e6e2] bg-white/50 backdrop-blur-sm cursor-pointer"
        whileHover={{
          y: -2,
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          borderColor: '#b89d6e'
        }}
        transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      >
        <div className="text-center">
          <h4 className="text-base font-semibold text-[#1a1a1a] mb-1">
            {value.title}
          </h4>
          <p className="text-sm text-[#5a5a5a]">
            {value.description}
          </p>
        </div>

        <motion.div
          initial="collapsed"
          animate={isHovered ? 'expanded' : 'collapsed'}
          variants={valueExpandAnimation}
          className="overflow-hidden"
        >
          <div className="pt-3 mt-3 border-t border-[#e8e6e2]">
            <p className="text-xs text-[#5a5a5a] leading-relaxed">
              {value.fullDescription}
            </p>
          </div>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
