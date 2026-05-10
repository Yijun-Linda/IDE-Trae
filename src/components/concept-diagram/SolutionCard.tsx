import React from 'react';
import { motion } from 'framer-motion';
import { Solution } from './concept-diagram-schema';
import { FlowDiagram } from './FlowDiagram';
import { cardHoverAnimation, expandAnimation } from './animations';

interface SolutionCardProps {
  solution: Solution;
  isExpanded: boolean;
  onToggle: () => void;
  hoveredStepId: string | null;
  onStepHover: (id: string | null) => void;
  index: number;
}

export function SolutionCard({
  solution,
  isExpanded,
  onToggle,
  hoveredStepId,
  onStepHover,
  index
}: SolutionCardProps) {
  return (
    <motion.div
      className="flex-1 min-w-[300px] max-w-[450px]"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.8,
        delay: 0.3 + index * 0.15,
        ease: [0.16, 1, 0.3, 1]
      }}
    >
      <motion.div
        className="bg-white rounded-2xl overflow-hidden cursor-pointer"
        initial="rest"
        whileHover="hover"
        animate="rest"
        variants={cardHoverAnimation}
        onClick={onToggle}
      >
        {/* Card Header */}
        <div className="p-6 border-b border-[#e8e6e2]">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">{solution.icon}</span>
            <h3 className="text-xl font-semibold text-[#1a1a1a]">
              {solution.name}
            </h3>
          </div>
          <p className="text-sm text-[#9a9a9a]">
            点击查看详情
          </p>
        </div>

        {/* Flow Diagram */}
        <div className="px-6">
          <FlowDiagram
            steps={solution.steps}
            hoveredStepId={hoveredStepId}
            onStepHover={onStepHover}
            solutionId={solution.id}
          />
        </div>

        {/* Tagline */}
        <div className="px-6 pb-4 text-center">
          <p className="text-lg text-[#b89d6e] font-medium italic">
            {solution.tagline}
          </p>
        </div>

        {/* Expandable Details */}
        <motion.div
          initial="collapsed"
          animate={isExpanded ? 'expanded' : 'collapsed'}
          variants={expandAnimation}
          className="overflow-hidden"
        >
          <div className="px-6 pb-6 pt-2 border-t border-[#e8e6e2] bg-[#fafaf9]">
            <p className="text-sm text-[#5a5a5a] leading-relaxed">
              {solution.details}
            </p>
          </div>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
