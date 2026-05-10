import React from 'react';
import { motion } from 'framer-motion';
import { FlowStep } from './concept-diagram-schema';
import { stepHighlightAnimation } from './animations';

interface FlowDiagramProps {
  steps: FlowStep[];
  hoveredStepId: string | null;
  onStepHover: (id: string | null) => void;
  solutionId: string;
}

export function FlowDiagram({ steps, hoveredStepId, onStepHover, solutionId }: FlowDiagramProps) {
  return (
    <div className="flex flex-col items-center gap-3 py-4">
      {steps.map((step, index) => {
        const stepId = `${solutionId}-step-${index}`;
        const isHovered = hoveredStepId === stepId;
        
        return (
          <React.Fragment key={stepId}>
            <motion.div
              className="relative w-full max-w-[200px] p-3 rounded-lg cursor-pointer"
              initial="rest"
              whileHover="hover"
              animate={isHovered ? 'hover' : 'rest'}
              variants={stepHighlightAnimation}
              onMouseEnter={() => onStepHover(stepId)}
              onMouseLeave={() => onStepHover(null)}
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">{step.icon}</span>
                <div className="flex-1">
                  <div className="text-sm font-medium text-[#1a1a1a]">
                    {step.label}
                  </div>
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{
                      height: isHovered ? 'auto' : 0,
                      opacity: isHovered ? 1 : 0
                    }}
                    transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                    className="overflow-hidden"
                  >
                    <div className="text-xs text-[#5a5a5a] mt-1">
                      {step.description}
                    </div>
                  </motion.div>
                </div>
              </div>
            </motion.div>
            
            {index < steps.length - 1 && (
              <motion.div
                className="text-[#b89d6e] text-xl"
                animate={{ y: [0, 4, 0] }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  ease: 'easeInOut',
                  delay: index * 0.2
                }}
              >
                ↓
              </motion.div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}
