import React from 'react';
import { motion } from 'framer-motion';
import { ConceptDiagramConfig } from './concept-diagram-schema';
import { useConceptDiagram } from './useConceptDiagram';
import { ParallaxBackground } from './ParallaxBackground';
import { SolutionCard } from './SolutionCard';
import { ValueTag } from './ValueTag';
import { arrowPulseAnimation } from './animations';

interface ConceptDiagramProps {
  config: ConceptDiagramConfig;
}

export function ConceptDiagram({ config }: ConceptDiagramProps) {
  const {
    expandedCardId,
    hoveredValueId,
    hoveredStepId,
    toggleCard,
    setHoveredValue,
    setHoveredStep
  } = useConceptDiagram();

  return (
    <div 
      className="min-h-screen relative overflow-hidden"
      style={{ backgroundColor: config.style.colors.bg }}
    >
      {/* Parallax Background */}
      <ParallaxBackground />

      {/* Main Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
        {/* Header */}
        <motion.header
          className="text-center mb-12 lg:mb-16"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <h1 
            className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4 tracking-tight"
            style={{ color: config.style.colors.text }}
          >
            {config.title}
          </h1>
          <p 
            className="text-lg sm:text-xl"
            style={{ color: config.style.colors.text }}
          >
            {config.subtitle}
          </p>
        </motion.header>

        {/* Comparison Section */}
        <section className="mb-16 lg:mb-20">
          <div className="flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-8">
            {/* Solution Cards */}
            {config.solutions.map((solution, index) => (
              <React.Fragment key={solution.id}>
                <SolutionCard
                  solution={solution}
                  isExpanded={expandedCardId === solution.id}
                  onToggle={() => toggleCard(solution.id)}
                  hoveredStepId={hoveredStepId}
                  onStepHover={setHoveredStep}
                  index={index}
                />
                
                {/* Connection Arrow (between cards) */}
                {index === 0 && (
                  <motion.div
                    className="hidden lg:flex items-center justify-center"
                    animate={arrowPulseAnimation.animate}
                  >
                    <div 
                      className="text-4xl"
                      style={{ color: config.style.colors.accent }}
                    >
                      →
                    </div>
                  </motion.div>
                )}
                
                {/* Mobile Arrow */}
                {index === 0 && (
                  <motion.div
                    className="flex lg:hidden items-center justify-center"
                    animate={{ y: [0, 8, 0] }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      ease: 'easeInOut'
                    }}
                  >
                    <div 
                      className="text-3xl"
                      style={{ color: config.style.colors.accent }}
                    >
                      ↓
                    </div>
                  </motion.div>
                )}
              </React.Fragment>
            ))}
          </div>
        </section>

        {/* Values Section */}
        <section>
          <motion.h2
            className="text-center text-xl sm:text-2xl font-semibold mb-8"
            style={{ color: config.style.colors.text }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.6 }}
          >
            核心价值
          </motion.h2>
          
          <div className="flex flex-col sm:flex-row items-stretch justify-center gap-4 sm:gap-6">
            {config.values.map((value, index) => (
              <ValueTag
                key={value.title}
                value={value}
                isHovered={hoveredValueId === value.title}
                onHover={(isHovered) => setHoveredValue(isHovered ? value.title : null)}
                index={index}
              />
            ))}
          </div>
        </section>

        {/* Footer */}
        <motion.footer
          className="mt-16 lg:mt-20 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 0.6 }}
        >
          <p className="text-sm text-[#9a9a9a]">
            点击方案卡片查看详情 · 悬停查看更多信息
          </p>
        </motion.footer>
      </div>
    </div>
  );
}
