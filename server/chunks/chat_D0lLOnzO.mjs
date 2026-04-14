import { spawn } from 'child_process';

// Minimal Node.js API route for Operator Chat (Astro SSR or Express-compatible)


async function post(req, res) {
  const { message, sessionId } = req.body;
  // Call the real GCD Python backend (example: scripts/cai_chat.py)
  const py = spawn('python3', [
    'scripts/cai_chat.py',
    '--message', message,
    '--session', sessionId || ''
  ]);

  let output = '';
  let error = '';
  py.stdout.on('data', (data) => { output += data; });
  py.stderr.on('data', (data) => { error += data; });
  py.on('close', (code) => {
    if (code !== 0 || !output) {
      res.status(500).json({ error: error || 'GCD backend error' });
      return;
    }
    try {
      const parsed = JSON.parse(output);
      res.json(parsed);
    } catch (e) {
      res.status(500).json({ error: 'Invalid backend response', details: output });
    }
  });
}

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  post
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
