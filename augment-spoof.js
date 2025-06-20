// augment-spoof.js  (改进版)
// 1. 打印调试信息
console.log('[augment-spoof] file loaded');

// 2. 当所有扩展都激活后再 patch，避免时序问题
const { extensions } = require('vscode');
extensions.onDidChange(() => {
  const aug = extensions.getExtension('augment.vscode-augment');
  if (!aug || !aug.isActive) return;           // 还未激活
  try {
    const api = aug.exports?._apiServer;
    if (!api || api.__patched) return;         // 已处理过
    const crypto = require('crypto');
    const newId = crypto.randomUUID?.() ||     // Node ≥ 14.17
      ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,
        c => (c ^ crypto.randomBytes(1)[0] & 15 >> c/4).toString(16));
    Object.defineProperty(api, 'sessionId', {
      get() { return newId; },
      set() {},
      configurable: false
    });
    api.__patched = true;
    console.log('[augment-spoof] sessionId =>', newId);
  } catch (e) {
    console.error('[augment-spoof] patch failed:', e);
  }
});