import { useState, useCallback } from 'react';

interface UseConceptDiagramReturn {
  expandedCardId: string | null;
  hoveredValueId: string | null;
  hoveredStepId: string | null;
  toggleCard: (id: string) => void;
  setHoveredValue: (id: string | null) => void;
  setHoveredStep: (id: string | null) => void;
  closeAllCards: () => void;
}

export function useConceptDiagram(): UseConceptDiagramReturn {
  const [expandedCardId, setExpandedCardId] = useState<string | null>(null);
  const [hoveredValueId, setHoveredValueId] = useState<string | null>(null);
  const [hoveredStepId, setHoveredStepId] = useState<string | null>(null);

  const toggleCard = useCallback((id: string) => {
    setExpandedCardId(prev => prev === id ? null : id);
  }, []);

  const setHoveredValue = useCallback((id: string | null) => {
    setHoveredValueId(id);
  }, []);

  const setHoveredStep = useCallback((id: string | null) => {
    setHoveredStepId(id);
  }, []);

  const closeAllCards = useCallback(() => {
    setExpandedCardId(null);
  }, []);

  return {
    expandedCardId,
    hoveredValueId,
    hoveredStepId,
    toggleCard,
    setHoveredValue,
    setHoveredStep,
    closeAllCards
  };
}
