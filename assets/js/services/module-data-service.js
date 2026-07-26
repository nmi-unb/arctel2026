const DATA_DIRECTORY = new URL("../../data/modulos/", import.meta.url);
const INDEX_URL = new URL("index.json", DATA_DIRECTORY);

const LINK_TYPES = ["teams", "youtubeLive", "youtubeRecorded"];
const LESSON_ID_PATTERN = /^aula-(\d+)$/;

let indexPromise = null;
const moduleCache = new Map();

async function fetchJson(url, context) {
  let response;
  try {
    response = await fetch(url);
  } catch (error) {
    throw new Error(`${context}: falha de rede ao buscar ${url}`, { cause: error });
  }
  if (!response.ok) {
    throw new Error(`${context}: HTTP ${response.status} ao buscar ${url}`);
  }
  return response.json();
}

export async function getModuleIndex() {
  if (!indexPromise) {
    indexPromise = fetchJson(INDEX_URL, "getModuleIndex").catch((error) => {
      indexPromise = null;
      throw error;
    });
  }
  return indexPromise;
}

export async function getModuleData(moduleId) {
  if (moduleCache.has(moduleId)) {
    return moduleCache.get(moduleId);
  }

  const promise = (async () => {
    const index = await getModuleIndex();
    const entry = index.modules.find((module) => module.id === moduleId);
    if (!entry) {
      throw new Error(`getModuleData: módulo desconhecido "${moduleId}"`);
    }
    return fetchJson(new URL(entry.dataFile, DATA_DIRECTORY), `getModuleData("${moduleId}")`);
  })();

  moduleCache.set(moduleId, promise);
  promise.catch(() => moduleCache.delete(moduleId));
  return promise;
}

export async function getLessonData(moduleId, lessonId) {
  const match = LESSON_ID_PATTERN.exec(lessonId || "");
  if (!match) {
    throw new Error(`getLessonData: lessonId inválido "${lessonId}"`);
  }
  const numero = Number(match[1]);

  const moduleData = await getModuleData(moduleId);
  const lesson = (moduleData.lessons || []).find((item) => item.numero === numero);
  if (!lesson) {
    throw new Error(`getLessonData: aula "${lessonId}" não encontrada em "${moduleId}"`);
  }
  return lesson;
}

export async function getLessonLink(moduleId, lessonId, linkType) {
  if (!LINK_TYPES.includes(linkType)) {
    throw new Error(`getLessonLink: linkType inválido "${linkType}"`);
  }
  const lesson = await getLessonData(moduleId, lessonId);
  return lesson.links ? lesson.links[linkType] ?? null : null;
}

export function clearModuleCache(moduleId = null) {
  if (moduleId === null) {
    moduleCache.clear();
    indexPromise = null;
    return;
  }
  moduleCache.delete(moduleId);
}
