import { ConceptDiagramConfig } from './concept-diagram-schema';

export const defaultConfig: ConceptDiagramConfig = {
  title: '从"被动等待"到"主动关怀"',
  subtitle: '下一代 AI 辅助方案演进',
  solutions: [
    {
      id: 'printer',
      name: '方案一：云打印机',
      icon: '🧾',
      steps: [
        { 
          icon: '📋', 
          label: '订单来了', 
          description: '系统自动接收订单' 
        },
        { 
          icon: '🖨️', 
          label: '自动出票', 
          description: '云打印机自动打印小票' 
        },
        { 
          icon: '👀', 
          label: '员工查看', 
          description: '员工主动查看小票内容' 
        }
      ],
      tagline: '"订单来了，请查看"',
      details: '基于现有云打印机的低成本方案，将复杂订单拆解为步骤化小票。员工需要主动查看小票，按步骤完成制作。'
    },
    {
      id: 'camera',
      name: '方案二：边缘感知',
      icon: '👁️',
      steps: [
        { 
          icon: '👁️', 
          label: '摄像头感知', 
          description: '实时监测员工状态' 
        },
        { 
          icon: '🧠', 
          label: 'AI 判断', 
          description: '边缘设备分析是否需要介入' 
        },
        { 
          icon: '🔊', 
          label: '语音提醒', 
          description: '主动语音提供下一步指引' 
        }
      ],
      tagline: '"需要帮忙吗？"',
      details: '基于摄像头+边缘算力的主动感知方案。当检测到员工停滞时，系统主动语音提醒，从被动推送进化到主动关怀。'
    }
  ],
  values: [
    { 
      title: '零延迟感知', 
      description: '实时监测',
      fullDescription: '摄像头持续感知员工动作，3秒内完成检测到语音输出的全流程，真正做到零延迟响应。'
    },
    { 
      title: '隐私本地处理', 
      description: '边缘计算',
      fullDescription: '所有数据处理在本地边缘设备完成，不上传云端，视频流不存储，充分保护员工和顾客隐私。'
    },
    { 
      title: '人性化语音交互', 
      description: '主动关怀',
      fullDescription: '用温暖自然的语音主动提供帮助，像一位耐心的辅导员，而非冷冰冰的机器指令。'
    }
  ],
  style: {
    theme: 'literary',
    colors: {
      bg: '#fafaf9',
      text: '#1a1a1a',
      accent: '#b89d6e'
    }
  }
};

export const literaryTheme = {
  bg: '#fafaf9',
  bgWarm: '#f5f4f0',
  text: '#1a1a1a',
  textSoft: '#5a5a5a',
  textMuted: '#9a9a9a',
  accent: '#b89d6e',
  accentDark: '#8a7348',
  border: '#e8e6e2'
};

export const industrialTheme = {
  bg: '#0a0a0a',
  bgSecondary: '#141414',
  text: '#f5f5f5',
  textSoft: '#8a8a8a',
  textMuted: '#555555',
  accent: '#c9a227',
  accentDark: '#8a7019',
  border: '#2a2a2a'
};
