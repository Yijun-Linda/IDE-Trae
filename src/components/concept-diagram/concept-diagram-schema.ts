import { z } from 'zod';

// 流程步骤 Schema
export const FlowStepSchema = z.object({
  icon: z.string(),
  label: z.string(),
  description: z.string()
});

// 解决方案 Schema
export const SolutionSchema = z.object({
  id: z.string(),
  name: z.string(),
  icon: z.string(),
  steps: z.array(FlowStepSchema),
  tagline: z.string(),
  details: z.string()
});

// 核心价值 Schema
export const ValueSchema = z.object({
  title: z.string(),
  description: z.string(),
  fullDescription: z.string()
});

// 样式配置 Schema
export const StyleConfigSchema = z.object({
  theme: z.enum(['literary', 'industrial']),
  colors: z.object({
    bg: z.string(),
    text: z.string(),
    accent: z.string()
  })
});

// 概念图配置 Schema
export const ConceptDiagramSchema = z.object({
  title: z.string(),
  subtitle: z.string(),
  solutions: z.array(SolutionSchema),
  values: z.array(ValueSchema),
  style: StyleConfigSchema
});

// 类型导出
export type FlowStep = z.infer<typeof FlowStepSchema>;
export type Solution = z.infer<typeof SolutionSchema>;
export type Value = z.infer<typeof ValueSchema>;
export type StyleConfig = z.infer<typeof StyleConfigSchema>;
export type ConceptDiagramConfig = z.infer<typeof ConceptDiagramSchema>;
