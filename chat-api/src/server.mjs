import { crearApp } from './app.mjs';

const { servidor, config } = crearApp();
if (!config.apiKey) console.warn('Falta GEMINI_API_KEY: el servicio responde que no está disponible.');
servidor.listen(config.port, () => {
  console.log(`chat-api en :${config.port} | modelo ${config.modelo} | tope USD ${config.limiteUsd}/mes`);
});
for (const s of ['SIGTERM', 'SIGINT']) process.on(s, () => servidor.close(() => process.exit(0)));
