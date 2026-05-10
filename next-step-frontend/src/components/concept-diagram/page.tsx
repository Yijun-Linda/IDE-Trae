'use client';

import React from 'react';
import { ConceptDiagram } from './ConceptDiagram';
import { defaultConfig } from './concept-diagram-config';

export default function ConceptDiagramPage() {
  return <ConceptDiagram config={defaultConfig} />;
}
