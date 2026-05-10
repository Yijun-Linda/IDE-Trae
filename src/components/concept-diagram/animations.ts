import { Variants, Transition } from 'framer-motion';

// 缓动函数
export const easeOutExpo: Transition = {
  duration: 0.8,
  ease: [0.16, 1, 0.3, 1]
};

export const easeOutQuart: Transition = {
  duration: 0.4,
  ease: [0.25, 1, 0.5, 1]
};

// 卡片悬停动画
export const cardHoverAnimation = {
  rest: {
    y: 0,
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    transition: easeOutQuart
  },
  hover: {
    y: -4,
    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    transition: easeOutQuart
  }
};

// 展开/收起动画
export const expandAnimation: Variants = {
  collapsed: {
    height: 0,
    opacity: 0,
    transition: {
      height: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
      opacity: { duration: 0.2 }
    }
  },
  expanded: {
    height: 'auto',
    opacity: 1,
    transition: {
      height: { duration: 0.4, ease: [0.16, 1, 0.3, 1] },
      opacity: { duration: 0.3, delay: 0.1 }
    }
  }
};

// 渐显动画
export const fadeInAnimation: Variants = {
  hidden: {
    opacity: 0,
    y: 40
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: easeOutExpo
  }
};

// 交错渐显动画
export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.2
    }
  }
};

// 步骤高亮动画
export const stepHighlightAnimation = {
  rest: {
    scale: 1,
    backgroundColor: 'rgba(184, 157, 110, 0)',
    transition: easeOutQuart
  },
  hover: {
    scale: 1.02,
    backgroundColor: 'rgba(184, 157, 110, 0.1)',
    transition: easeOutQuart
  }
};

// 价值标签展开动画
export const valueExpandAnimation: Variants = {
  collapsed: {
    height: 0,
    opacity: 0,
    transition: {
      height: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
      opacity: { duration: 0.2 }
    }
  },
  expanded: {
    height: 'auto',
    opacity: 1,
    transition: {
      height: { duration: 0.4, ease: [0.16, 1, 0.3, 1] },
      opacity: { duration: 0.3, delay: 0.1 }
    }
  }
};

// 箭头脉动动画
export const arrowPulseAnimation = {
  animate: {
    x: [0, 8, 0],
    transition: {
      duration: 1.5,
      repeat: Infinity,
      ease: 'easeInOut'
    }
  }
};
