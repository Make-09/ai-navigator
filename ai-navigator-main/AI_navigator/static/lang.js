// простой i18n — ключи и строки
const LOCALES = {
  "ru": {
    code: "ru",
    name: "Рус",
    strings: {
      loading: "AI думает...",
      server_error: "Ошибка сервера. Попробуйте позже.",
      network_error: "Сетевая ошибка — проверьте подключение.",
      bad_response: "Получили неверный ответ от сервера.",
      chat_cleared: "Чат очищен.",
      clear_failed: "Не удалось очистить чат.",
      clear_error: "Ошибка при очистке чата.",
      new_chat: "+ Новый чат",
      no_chats: "Нет сохранённых чатов",
      nav_home: "Главная",
      nav_about: "О нас",
      nav_faq: "FAQ",
      nav_policy: "Политика",
      footer_copyright: "© AI Navigator — создатели: школьники из Шымкента и Уральска",
      footer_support: "Поддержка проекта — скоро"
    }
  },
  "en": {
    code: "en",
    name: "EN",
    strings: {
      loading: "AI thinking...",
      server_error: "Server error. Please try later.",
      network_error: "Network error — check your connection.",
      bad_response: "Invalid response from server.",
      chat_cleared: "Chat cleared.",
      clear_failed: "Failed to clear chat.",
      clear_error: "Error while clearing chat.",
      new_chat: "+ New chat",
      no_chats: "No saved chats",
      nav_home: "Home",
      nav_about: "About",
      nav_faq: "FAQ",
      nav_policy: "Policy",
      footer_copyright: "© AI Navigator — creators: students from Shymkent and Uralsk",
      footer_support: "Support — coming soon"
    }
  },
  "kz": {
    code: "kz",
    name: "KZ",
    strings: {
      loading: "AI ойланып жатыр...",
      server_error: "Сервер қатесі. Кейінірек көріңіз.",
      network_error: "Желі қатесі — қосылымды тексеріңіз.",
      bad_response: "Серверден дұрыс емес жауап алынды.",
      chat_cleared: "Чат тазартылды.",
      clear_failed: "Чатты тазарту мүмкін болмады.",
      clear_error: "Чатты тазарту қатесі.",
      new_chat: "+ Жаңа чат",
      no_chats: "Сақталған чаттар жоқ",
      nav_home: "Басты",
      nav_about: "Біз туралы",
      nav_faq: "Жиі сұрақтар",
      nav_policy: "Саясат",
      footer_copyright: "© AI Navigator — жасаушылар: Шымкент және Орал оқушылары",
      footer_support: "Жобаға қолдау — жақында"
    }
  },
  "zh": {
    code: "zh",
    name: "中文",
    strings: {
      loading: "AI 正在思考...",
      server_error: "服务器错误，请稍后再试。",
      network_error: "网络错误 — 请检查连接。",
      bad_response: "从服务器收到无效响应。",
      chat_cleared: "聊天已清除。",
      clear_failed: "无法清除聊天。",
      clear_error: "清除聊天时出错。",
      new_chat: "+ 新聊天",
      no_chats: "没有保存的聊天",
      nav_home: "主页",
      nav_about: "关于我们",
      nav_faq: "常见问题",
      nav_policy: "隐私政策",
      footer_copyright: "© AI Navigator — 创建者：什姆肯特和乌拉尔斯克的学生",
      footer_support: "支持 — 即将推出"
    }
  },
  "ja": {
    code: "ja",
    name: "日本語",
    strings: {
      loading: "AIは考えています...",
      server_error: "サーバーエラー。後で再試行してください。",
      network_error: "ネットワークエラー — 接続を確認してください。",
      bad_response: "サーバーから無効な応答を受信しました。",
      chat_cleared: "チャットがクリアされました。",
      clear_failed: "チャットをクリアできませんでした。",
      clear_error: "チャットのクリア中にエラーが発生しました。",
      new_chat: "+ 新しいチャット",
      no_chats: "保存されたチャットはありません",
      nav_home: "ホーム",
      nav_about: "私たちについて",
      nav_faq: "FAQ",
      nav_policy: "ポリシー",
      footer_copyright: "© AI Navigator — 作成者：シムケントとウラルスクの学生",
      footer_support: "サポート — まもなく"
    }
  },
  "ko": {
    code: "ko",
    name: "한국어",
    strings: {
      loading: "AI가 생각 중...",
      server_error: "서버 오류입니다. 나중에 다시 시도하세요.",
      network_error: "네트워크 오류 — 연결을 확인하세요.",
      bad_response: "서버로부터 잘못된 응답을 받았습니다.",
      chat_cleared: "채팅이 지워졌습니다.",
      clear_failed: "채팅을 지우지 못했습니다.",
      clear_error: "채팅 지우기 중 오류가 발생했습니다.",
      new_chat: "+ 새 채팅",
      no_chats: "저장된 채팅이 없습니다",
      nav_home: "홈",
      nav_about: "회사소개",
      nav_faq: "FAQ",
      nav_policy: "정책",
      footer_copyright: "© AI Navigator — 제작자: 심켄트와 우랄스크의 학생들",
      footer_support: "지원 — 곧 제공"
    }
  }
};

// current locale holder (default ru)
let currentLocale = LOCALES["ru"];

// initialize language selector in DOM
function initLocales() {
  const sel = document.getElementById("lang-select");
  if (!sel) return;
  sel.innerHTML = "";
  Object.values(LOCALES).forEach(loc => {
    const opt = document.createElement("option");
    opt.value = loc.code;
    opt.textContent = loc.name;
    sel.appendChild(opt);
  });

  // load saved locale
  const saved = localStorage.getItem("ai_locale");
  const browser = (navigator.language || navigator.userLanguage || "ru").slice(0,2);
  const chosen = saved || (LOCALES[browser] ? browser : "ru");
  sel.value = chosen;
  setLocale(chosen);

  sel.addEventListener("change", (e) => {
    setLocale(e.target.value);
    localStorage.setItem("ai_locale", e.target.value);
  });
}

function setLocale(code) {
  if (!LOCALES[code]) code = "ru";
  currentLocale = LOCALES[code];
  // update simple UI strings
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (currentLocale.strings[key]) el.textContent = currentLocale.strings[key];
  });
  // update placeholders, titles if needed
  const ta = document.getElementById("user-input");
  if (ta) {
    const placeholder = {
      "ru":"Напишите ваш вопрос...",
      "en":"Write your question...",
      "kz":"Сұрағыңызды жазыңыз...",
      "zh":"在这里输入你的问题...",
      "ja":"質問を入力してください...",
      "ko":"질문을 입력하세요..."
    }[code] || "Напишите ваш вопрос...";
    ta.placeholder = placeholder;
  }
}

// run init on DOMContentLoaded
document.addEventListener("DOMContentLoaded", initLocales);
