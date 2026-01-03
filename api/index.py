"""
Тренажёр для изучения бухгалтерских счетов
По типовому плану счетов Республики Беларусь
"""

from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

# План счетов бухгалтерского учёта (типовой план счетов РБ)
ACCOUNTS = {
    # Раздел I. Внеоборотные активы
    "01": {"name": "Основные средства", "section": "I. Внеоборотные активы", "type": "А"},
    "02": {"name": "Амортизация основных средств", "section": "I. Внеоборотные активы", "type": "П"},
    "03": {"name": "Доходные вложения в материальные активы", "section": "I. Внеоборотные активы", "type": "А"},
    "04": {"name": "Нематериальные активы", "section": "I. Внеоборотные активы", "type": "А"},
    "05": {"name": "Амортизация нематериальных активов", "section": "I. Внеоборотные активы", "type": "П"},
    "06": {"name": "Долгосрочные финансовые вложения", "section": "I. Внеоборотные активы", "type": "А"},
    "07": {"name": "Оборудование к установке", "section": "I. Внеоборотные активы", "type": "А"},
    "08": {"name": "Вложения в долгосрочные активы", "section": "I. Внеоборотные активы", "type": "А"},
    "09": {"name": "Отложенные налоговые активы", "section": "I. Внеоборотные активы", "type": "А"},
    
    # Раздел II. Производственные запасы
    "10": {"name": "Материалы", "section": "II. Производственные запасы", "type": "А"},
    "11": {"name": "Животные на выращивании и откорме", "section": "II. Производственные запасы", "type": "А"},
    "14": {"name": "Резервы под снижение стоимости материальных ценностей", "section": "II. Производственные запасы", "type": "П"},
    "15": {"name": "Заготовление и приобретение материальных ценностей", "section": "II. Производственные запасы", "type": "А"},
    "16": {"name": "Отклонение в стоимости материальных ценностей", "section": "II. Производственные запасы", "type": "А/П"},
    
    # Раздел III. Затраты на производство
    "20": {"name": "Основное производство", "section": "III. Затраты на производство", "type": "А"},
    "21": {"name": "Полуфабрикаты собственного производства", "section": "III. Затраты на производство", "type": "А"},
    "23": {"name": "Вспомогательные производства", "section": "III. Затраты на производство", "type": "А"},
    "25": {"name": "Общепроизводственные затраты", "section": "III. Затраты на производство", "type": "А"},
    "26": {"name": "Общехозяйственные затраты", "section": "III. Затраты на производство", "type": "А"},
    "28": {"name": "Брак в производстве", "section": "III. Затраты на производство", "type": "А"},
    "29": {"name": "Обслуживающие производства и хозяйства", "section": "III. Затраты на производство", "type": "А"},
    
    # Раздел IV. Готовая продукция и товары
    "40": {"name": "Выпуск продукции, работ, услуг", "section": "IV. Готовая продукция и товары", "type": "А/П"},
    "41": {"name": "Товары", "section": "IV. Готовая продукция и товары", "type": "А"},
    "42": {"name": "Торговая наценка", "section": "IV. Готовая продукция и товары", "type": "П"},
    "43": {"name": "Готовая продукция", "section": "IV. Готовая продукция и товары", "type": "А"},
    "44": {"name": "Расходы на реализацию", "section": "IV. Готовая продукция и товары", "type": "А"},
    "45": {"name": "Товары отгруженные", "section": "IV. Готовая продукция и товары", "type": "А"},
    
    # Раздел V. Денежные средства
    "50": {"name": "Касса", "section": "V. Денежные средства", "type": "А"},
    "51": {"name": "Расчётные счета", "section": "V. Денежные средства", "type": "А"},
    "52": {"name": "Валютные счета", "section": "V. Денежные средства", "type": "А"},
    "55": {"name": "Специальные счета в банках", "section": "V. Денежные средства", "type": "А"},
    "57": {"name": "Денежные средства в пути", "section": "V. Денежные средства", "type": "А"},
    "58": {"name": "Краткосрочные финансовые вложения", "section": "V. Денежные средства", "type": "А"},
    "59": {"name": "Резервы под обесценение краткосрочных финансовых вложений", "section": "V. Денежные средства", "type": "П"},
    
    # Раздел VI. Расчёты
    "60": {"name": "Расчёты с поставщиками и подрядчиками", "section": "VI. Расчёты", "type": "А/П"},
    "62": {"name": "Расчёты с покупателями и заказчиками", "section": "VI. Расчёты", "type": "А/П"},
    "63": {"name": "Резервы по сомнительным долгам", "section": "VI. Расчёты", "type": "П"},
    "65": {"name": "Отложенные налоговые обязательства", "section": "VI. Расчёты", "type": "П"},
    "66": {"name": "Расчёты по краткосрочным кредитам и займам", "section": "VI. Расчёты", "type": "П"},
    "67": {"name": "Расчёты по долгосрочным кредитам и займам", "section": "VI. Расчёты", "type": "П"},
    "68": {"name": "Расчёты по налогам и сборам", "section": "VI. Расчёты", "type": "А/П"},
    "69": {"name": "Расчёты по социальному страхованию и обеспечению", "section": "VI. Расчёты", "type": "А/П"},
    "70": {"name": "Расчёты с персоналом по оплате труда", "section": "VI. Расчёты", "type": "П"},
    "71": {"name": "Расчёты с подотчётными лицами", "section": "VI. Расчёты", "type": "А/П"},
    "73": {"name": "Расчёты с персоналом по прочим операциям", "section": "VI. Расчёты", "type": "А/П"},
    "75": {"name": "Расчёты с учредителями", "section": "VI. Расчёты", "type": "А/П"},
    "76": {"name": "Расчёты с разными дебиторами и кредиторами", "section": "VI. Расчёты", "type": "А/П"},
    "77": {"name": "Расчёты по прямому страхованию и перестрахованию", "section": "VI. Расчёты", "type": "А/П"},
    "79": {"name": "Внутрихозяйственные расчёты", "section": "VI. Расчёты", "type": "А/П"},
    
    # Раздел VII. Источники собственных средств
    "80": {"name": "Уставный капитал", "section": "VII. Источники собственных средств", "type": "П"},
    "81": {"name": "Собственные акции (доли в уставном капитале)", "section": "VII. Источники собственных средств", "type": "А"},
    "82": {"name": "Резервный капитал", "section": "VII. Источники собственных средств", "type": "П"},
    "83": {"name": "Добавочный капитал", "section": "VII. Источники собственных средств", "type": "П"},
    "84": {"name": "Нераспределённая прибыль (непокрытый убыток)", "section": "VII. Источники собственных средств", "type": "А/П"},
    "86": {"name": "Целевое финансирование", "section": "VII. Источники собственных средств", "type": "П"},
    
    # Раздел VIII. Финансовые результаты
    "90": {"name": "Доходы и расходы по текущей деятельности", "section": "VIII. Финансовые результаты", "type": "А/П"},
    "91": {"name": "Прочие доходы и расходы", "section": "VIII. Финансовые результаты", "type": "А/П"},
    "94": {"name": "Недостачи и потери от порчи имущества", "section": "VIII. Финансовые результаты", "type": "А"},
    "96": {"name": "Резервы предстоящих платежей", "section": "VIII. Финансовые результаты", "type": "П"},
    "97": {"name": "Расходы будущих периодов", "section": "VIII. Финансовые результаты", "type": "А"},
    "98": {"name": "Доходы будущих периодов", "section": "VIII. Финансовые результаты", "type": "П"},
    "99": {"name": "Прибыли и убытки", "section": "VIII. Финансовые результаты", "type": "А/П"},
}

# Забалансовые счета
OFF_BALANCE_ACCOUNTS = {
    "001": {"name": "Арендованные основные средства", "section": "Забалансовые счета"},
    "002": {"name": "Имущество, принятое на ответственное хранение", "section": "Забалансовые счета"},
    "003": {"name": "Материалы, принятые в переработку", "section": "Забалансовые счета"},
    "004": {"name": "Товары, принятые на комиссию", "section": "Забалансовые счета"},
    "005": {"name": "Оборудование, принятое для монтажа", "section": "Забалансовые счета"},
    "006": {"name": "Бланки строгой отчётности", "section": "Забалансовые счета"},
    "007": {"name": "Списанная в убыток задолженность неплатёжеспособных дебиторов", "section": "Забалансовые счета"},
    "008": {"name": "Обеспечения обязательств полученные", "section": "Забалансовые счета"},
    "009": {"name": "Обеспечения обязательств выданные", "section": "Забалансовые счета"},
    "010": {"name": "Амортизационный фонд воспроизводства основных средств", "section": "Забалансовые счета"},
    "011": {"name": "Основные средства, сданные в аренду", "section": "Забалансовые счета"},
    "012": {"name": "Нематериальные активы, полученные в пользование", "section": "Забалансовые счета"},
    "013": {"name": "Имущество, полученное в безвозмездное пользование", "section": "Забалансовые счета"},
    "014": {"name": "Потеря стоимости основных средств", "section": "Забалансовые счета"},
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Бухгалтерский тренажёр | План счетов</title>
    <link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #131a2b;
            --bg-card: #1a2540;
            --accent-cyan: #00f5d4;
            --accent-magenta: #f72585;
            --accent-yellow: #fee440;
            --accent-blue: #4cc9f0;
            --accent-green: #06d6a0;
            --text-primary: #ffffff;
            --text-secondary: #8892a6;
            --gradient-2: linear-gradient(135deg, #00f5d4 0%, #00bbf9 100%);
            --gradient-3: linear-gradient(135deg, #f72585 0%, #7209b7 100%);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Unbounded', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }
        .bg-animation {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 245, 212, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(247, 37, 133, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(76, 201, 240, 0.05) 0%, transparent 40%);
        }
        .bg-animation::before {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 50px 50px;
        }
        header { padding: 2rem; text-align: center; }
        .logo {
            font-size: 2.5rem; font-weight: 800;
            background: var(--gradient-2); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; background-clip: text;
            text-transform: uppercase; letter-spacing: 3px;
        }
        .subtitle { color: var(--text-secondary); font-size: 0.9rem; font-weight: 300; letter-spacing: 2px; }
        .mode-nav {
            display: flex; justify-content: center; gap: 0.8rem; padding: 1rem;
            flex-wrap: wrap; margin-bottom: 2rem;
        }
        .mode-btn {
            padding: 0.7rem 1.2rem; border: 2px solid transparent;
            background: var(--bg-card); color: var(--text-secondary);
            font-family: 'Unbounded', sans-serif; font-size: 0.75rem;
            cursor: pointer; border-radius: 50px; transition: all 0.3s ease;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .mode-btn:hover { border-color: var(--accent-cyan); color: var(--accent-cyan); transform: translateY(-2px); }
        .mode-btn.active { background: var(--gradient-2); color: var(--bg-primary); font-weight: 600; }
        .container { max-width: 900px; margin: 0 auto; padding: 0 2rem 4rem; }
        .card {
            background: var(--bg-card); border-radius: 24px; padding: 2.5rem;
            position: relative; overflow: hidden; animation: fadeIn 0.5s ease;
        }
        .card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: var(--gradient-2); }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        
        /* Quiz Progress */
        .quiz-progress { display: flex; justify-content: center; gap: 0.5rem; margin-bottom: 2rem; }
        .progress-dot {
            width: 12px; height: 12px; border-radius: 50%;
            background: var(--bg-secondary); transition: all 0.3s ease;
        }
        .progress-dot.current { background: var(--accent-cyan); transform: scale(1.3); }
        .progress-dot.correct { background: var(--accent-green); }
        .progress-dot.wrong { background: var(--accent-magenta); }
        
        .quiz-counter {
            text-align: center; margin-bottom: 1rem;
            font-family: 'JetBrains Mono', monospace; color: var(--text-secondary);
        }
        .quiz-question { font-size: 1.3rem; text-align: center; margin-bottom: 2rem; font-weight: 300; line-height: 1.6; }
        .quiz-question strong { font-weight: 600; color: var(--accent-cyan); }
        .quiz-options { display: grid; gap: 0.8rem; }
        .quiz-option {
            padding: 1rem 1.2rem; background: var(--bg-secondary);
            border: 2px solid transparent; border-radius: 16px;
            font-family: 'Unbounded', sans-serif; font-size: 0.95rem;
            color: var(--text-primary); cursor: pointer;
            transition: all 0.3s ease; text-align: left;
        }
        .quiz-option:hover:not(.disabled) { border-color: var(--accent-cyan); background: rgba(0, 245, 212, 0.1); transform: translateX(10px); }
        .quiz-option.correct { border-color: var(--accent-green); background: rgba(6, 214, 160, 0.2); }
        .quiz-option.wrong { border-color: var(--accent-magenta); background: rgba(247, 37, 133, 0.2); }
        .quiz-option.disabled { cursor: default; opacity: 0.7; }
        
        .quiz-feedback { text-align: center; margin-top: 1.5rem; padding: 1rem; border-radius: 16px; animation: slideUp 0.3s ease; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .quiz-feedback.success { background: rgba(6, 214, 160, 0.1); border: 1px solid rgba(6, 214, 160, 0.3); }
        .quiz-feedback.error { background: rgba(247, 37, 133, 0.1); border: 1px solid rgba(247, 37, 133, 0.3); }
        .quiz-feedback h3 { font-size: 1.1rem; margin-bottom: 0.3rem; }
        .quiz-feedback.success h3 { color: var(--accent-green); }
        .quiz-feedback.error h3 { color: var(--accent-magenta); }
        .quiz-feedback p { color: var(--text-secondary); font-size: 0.85rem; }
        
        .flashcard-controls { display: flex; justify-content: center; gap: 1rem; margin-top: 1.5rem; }
        .control-btn {
            padding: 0.9rem 1.8rem; border: none; border-radius: 50px;
            font-family: 'Unbounded', sans-serif; font-size: 0.85rem;
            font-weight: 600; cursor: pointer; transition: all 0.3s ease;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .btn-next { background: var(--gradient-2); color: var(--bg-primary); }
        .btn-next:hover { transform: scale(1.05); box-shadow: 0 10px 40px rgba(0, 245, 212, 0.3); }
        .btn-secondary { background: var(--bg-secondary); color: var(--text-primary); border: 2px solid var(--text-secondary); }
        .btn-secondary:hover { border-color: var(--accent-cyan); color: var(--accent-cyan); }
        
        /* Results */
        .results-container { text-align: center; }
        .results-score {
            font-family: 'JetBrains Mono', monospace; font-size: 4rem;
            font-weight: 800; margin-bottom: 1rem;
        }
        .results-score.excellent { color: var(--accent-green); }
        .results-score.good { color: var(--accent-cyan); }
        .results-score.average { color: var(--accent-yellow); }
        .results-score.poor { color: var(--accent-magenta); }
        .results-text { font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 2rem; }
        
        .errors-section { margin-top: 2rem; text-align: left; }
        .errors-title { font-size: 1rem; color: var(--accent-magenta); margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; }
        .error-item {
            background: var(--bg-secondary); border-radius: 12px; padding: 1rem;
            margin-bottom: 0.8rem; border-left: 4px solid var(--accent-magenta);
        }
        .error-item .question { font-size: 0.9rem; margin-bottom: 0.5rem; }
        .error-item .your-answer { color: var(--accent-magenta); font-size: 0.85rem; }
        .error-item .correct-answer { color: var(--accent-green); font-size: 0.85rem; }
        
        /* Flashcards */
        .flashcard-container { perspective: 1000px; min-height: 320px; }
        .flashcard {
            width: 100%; height: 320px; position: relative;
            transform-style: preserve-3d; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        .flashcard.flipped { transform: rotateY(180deg); }
        .flashcard-face {
            position: absolute; width: 100%; height: 100%;
            backface-visibility: hidden; border-radius: 24px;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center; padding: 2rem;
        }
        .flashcard-front { background: linear-gradient(145deg, var(--bg-card), #243050); border: 2px solid rgba(0, 245, 212, 0.2); }
        .flashcard-back { background: linear-gradient(145deg, #1a3a4a, var(--bg-card)); border: 2px solid rgba(247, 37, 133, 0.2); transform: rotateY(180deg); }
        .account-number {
            font-family: 'JetBrains Mono', monospace; font-size: 5rem; font-weight: 600;
            background: var(--gradient-2); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; background-clip: text; line-height: 1;
        }
        .account-hint { color: var(--text-secondary); font-size: 0.8rem; margin-top: 2rem; text-transform: uppercase; letter-spacing: 2px; }
        .account-name {
            font-size: 1.5rem; font-weight: 600; text-align: center; margin-bottom: 0.8rem;
            background: var(--gradient-3); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; background-clip: text;
        }
        .account-section { color: var(--text-secondary); font-size: 0.85rem; text-align: center; }
        .account-type { margin-top: 0.8rem; padding: 0.4rem 1.2rem; border-radius: 50px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
        .type-active { background: rgba(0, 245, 212, 0.2); color: var(--accent-cyan); }
        .type-passive { background: rgba(247, 37, 133, 0.2); color: var(--accent-magenta); }
        .type-mixed { background: rgba(254, 228, 64, 0.2); color: var(--accent-yellow); }
        
        /* Reference */
        .reference-filters { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
        .filter-btn {
            padding: 0.5rem 1rem; border: 1px solid var(--text-secondary);
            background: transparent; color: var(--text-secondary);
            font-family: 'Unbounded', sans-serif; font-size: 0.65rem;
            cursor: pointer; border-radius: 50px; transition: all 0.3s ease;
        }
        .filter-btn:hover, .filter-btn.active { border-color: var(--accent-cyan); color: var(--accent-cyan); }
        .accounts-list { display: grid; gap: 0.6rem; }
        .account-item {
            display: flex; align-items: center; padding: 0.8rem 1.2rem;
            background: var(--bg-secondary); border-radius: 12px; transition: all 0.3s ease;
        }
        .account-item:hover { background: rgba(0, 245, 212, 0.1); transform: translateX(5px); }
        .account-item .number { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 600; color: var(--accent-cyan); min-width: 55px; }
        .account-item .name { flex: 1; font-size: 0.9rem; }
        .account-item .type-badge { padding: 0.25rem 0.6rem; border-radius: 20px; font-size: 0.65rem; font-weight: 600; }
        
        .section { display: none; }
        .section.active { display: block; }
        
        @media (max-width: 600px) {
            .logo { font-size: 1.8rem; }
            .mode-btn { padding: 0.5rem 0.8rem; font-size: 0.65rem; }
            .card { padding: 1.5rem; }
            .account-number { font-size: 3.5rem; }
            .quiz-question { font-size: 1.1rem; }
            .results-score { font-size: 3rem; }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <header>
        <h1 class="logo">Бухучёт</h1>
        <p class="subtitle">Тренажёр плана счетов</p>
    </header>

    <nav class="mode-nav">
        <button class="mode-btn active" data-mode="flashcards">Карточки</button>
        <button class="mode-btn" data-mode="quiz-number">Номер → Название</button>
        <button class="mode-btn" data-mode="quiz-name">Название → Номер</button>
        <button class="mode-btn" data-mode="quiz-type">Тип счёта</button>
        <button class="mode-btn" data-mode="quiz-section">Раздел баланса</button>
        <button class="mode-btn" data-mode="reference">Справочник</button>
    </nav>

    <div class="container">
        <!-- Flashcards -->
        <section id="flashcards" class="section active">
            <div class="flashcard-container">
                <div class="flashcard" id="flashcard" onclick="flipCard()">
                    <div class="flashcard-face flashcard-front">
                        <div class="account-number" id="flashNumber">01</div>
                        <div class="account-hint">Нажмите, чтобы увидеть ответ</div>
                    </div>
                    <div class="flashcard-face flashcard-back">
                        <div class="account-name" id="flashName">Основные средства</div>
                        <div class="account-section" id="flashSection">I. Внеоборотные активы</div>
                        <div class="account-type type-active" id="flashType">Активный</div>
                    </div>
                </div>
            </div>
            <div class="flashcard-controls">
                <button class="control-btn btn-next" onclick="nextFlashcard()">Следующая →</button>
            </div>
        </section>

        <!-- Quiz Number to Name -->
        <section id="quiz-number" class="section"></section>
        
        <!-- Quiz Name to Number -->
        <section id="quiz-name" class="section"></section>
        
        <!-- Quiz Type -->
        <section id="quiz-type" class="section"></section>
        
        <!-- Quiz Section -->
        <section id="quiz-section" class="section"></section>

        <!-- Reference -->
        <section id="reference" class="section">
            <div class="card">
                <div class="reference-filters" id="filters"></div>
                <div class="accounts-list" id="accountsList"></div>
            </div>
        </section>
    </div>

    <script>
        const QUIZ_LENGTH = 10;
        let accountsData = null;
        
        // Quiz state for each quiz type
        let quizStates = {
            'quiz-number': null,
            'quiz-name': null,
            'quiz-type': null,
            'quiz-section': null
        };

        async function init() {
            const response = await fetch('/api/accounts');
            accountsData = await response.json();
            loadFlashcard();
            renderReference();
        }

        // Flashcard functions
        function flipCard() { document.getElementById('flashcard').classList.toggle('flipped'); }
        
        async function loadFlashcard() {
            const response = await fetch('/api/flashcard');
            const data = await response.json();
            document.getElementById('flashcard').classList.remove('flipped');
            setTimeout(() => {
                document.getElementById('flashNumber').textContent = data.number;
                document.getElementById('flashName').textContent = data.name;
                document.getElementById('flashSection').textContent = data.section || '';
                const typeEl = document.getElementById('flashType');
                if (data.type) {
                    typeEl.style.display = 'block';
                    const typeMap = { 'А': 'Активный', 'П': 'Пассивный', 'А/П': 'Активно-пассивный' };
                    typeEl.textContent = typeMap[data.type] || data.type;
                    typeEl.className = 'account-type';
                    if (data.type === 'А') typeEl.classList.add('type-active');
                    else if (data.type === 'П') typeEl.classList.add('type-passive');
                    else typeEl.classList.add('type-mixed');
                } else { typeEl.style.display = 'none'; }
            }, 100);
        }
        
        function nextFlashcard() { loadFlashcard(); }

        // Quiz functions
        async function startQuiz(quizType) {
            const apiMap = {
                'quiz-number': '/api/quiz/number-to-name',
                'quiz-name': '/api/quiz/name-to-number',
                'quiz-type': '/api/quiz/type',
                'quiz-section': '/api/quiz/section'
            };
            
            // Fetch all questions
            const questions = [];
            for (let i = 0; i < QUIZ_LENGTH; i++) {
                const response = await fetch(apiMap[quizType]);
                questions.push(await response.json());
            }
            
            quizStates[quizType] = {
                questions: questions,
                current: 0,
                answers: [],
                errors: []
            };
            
            renderQuizQuestion(quizType);
        }

        function renderQuizQuestion(quizType) {
            const state = quizStates[quizType];
            const section = document.getElementById(quizType);
            
            if (state.current >= QUIZ_LENGTH) {
                renderResults(quizType);
                return;
            }
            
            const q = state.questions[state.current];
            const progressDots = Array(QUIZ_LENGTH).fill(0).map((_, i) => {
                let cls = 'progress-dot';
                if (i < state.current) cls += state.answers[i] ? ' correct' : ' wrong';
                else if (i === state.current) cls += ' current';
                return `<div class="${cls}"></div>`;
            }).join('');
            
            section.innerHTML = `
                <div class="card">
                    <div class="quiz-progress">${progressDots}</div>
                    <div class="quiz-counter">Вопрос ${state.current + 1} из ${QUIZ_LENGTH}</div>
                    <div class="quiz-question">${q.question}</div>
                    <div class="quiz-options" id="${quizType}-options">
                        ${q.options.map((opt, i) => `<button class="quiz-option" onclick="checkQuizAnswer('${quizType}', '${opt.replace(/'/g, "\\'")}', this)">${opt}</button>`).join('')}
                    </div>
                    <div class="quiz-feedback" id="${quizType}-feedback" style="display: none;"></div>
                    <div class="flashcard-controls">
                        <button class="control-btn btn-next" id="${quizType}-next" style="display: none;" onclick="nextQuizQuestion('${quizType}')">Далее →</button>
                    </div>
                </div>
            `;
        }

        function checkQuizAnswer(quizType, answer, btnEl) {
            const state = quizStates[quizType];
            const q = state.questions[state.current];
            const isCorrect = answer === q.correct;
            
            state.answers.push(isCorrect);
            if (!isCorrect) {
                state.errors.push({
                    question: q.question,
                    yourAnswer: answer,
                    correctAnswer: q.correct,
                    section: q.section || ''
                });
            }
            
            // Disable all options and show correct/wrong
            document.querySelectorAll(`#${quizType}-options .quiz-option`).forEach(btn => {
                btn.classList.add('disabled');
                if (btn.textContent === q.correct) btn.classList.add('correct');
            });
            if (!isCorrect) btnEl.classList.add('wrong');
            
            // Show feedback
            const feedbackEl = document.getElementById(`${quizType}-feedback`);
            feedbackEl.style.display = 'block';
            if (isCorrect) {
                feedbackEl.className = 'quiz-feedback success';
                feedbackEl.innerHTML = `<h3>✓ Верно!</h3>`;
            } else {
                feedbackEl.className = 'quiz-feedback error';
                feedbackEl.innerHTML = `<h3>✗ Неверно</h3><p>Правильный ответ: <strong>${q.correct}</strong></p>`;
            }
            
            // Update progress dots
            const dots = document.querySelectorAll(`#${quizType} .progress-dot`);
            dots[state.current].classList.remove('current');
            dots[state.current].classList.add(isCorrect ? 'correct' : 'wrong');
            
            document.getElementById(`${quizType}-next`).style.display = 'inline-block';
        }

        function nextQuizQuestion(quizType) {
            const state = quizStates[quizType];
            state.current++;
            renderQuizQuestion(quizType);
        }

        function renderResults(quizType) {
            const state = quizStates[quizType];
            const correct = state.answers.filter(a => a).length;
            const percent = Math.round((correct / QUIZ_LENGTH) * 100);
            
            let scoreClass = 'poor';
            let message = 'Нужно ещё поучить!';
            if (percent >= 90) { scoreClass = 'excellent'; message = 'Отлично! Превосходный результат!'; }
            else if (percent >= 70) { scoreClass = 'good'; message = 'Хорошо! Так держать!'; }
            else if (percent >= 50) { scoreClass = 'average'; message = 'Неплохо, но есть над чем работать.'; }
            
            let errorsHtml = '';
            if (state.errors.length > 0) {
                errorsHtml = `
                    <div class="errors-section">
                        <div class="errors-title">Ошибки (${state.errors.length})</div>
                        ${state.errors.map(e => `
                            <div class="error-item">
                                <div class="question">${e.question}</div>
                                <div class="your-answer">Ваш ответ: ${e.yourAnswer}</div>
                                <div class="correct-answer">Правильно: ${e.correctAnswer}</div>
                            </div>
                        `).join('')}
                    </div>
                `;
            }
            
            document.getElementById(quizType).innerHTML = `
                <div class="card">
                    <div class="results-container">
                        <div class="results-score ${scoreClass}">${correct}/${QUIZ_LENGTH}</div>
                        <div class="results-text">${message}</div>
                        <div class="flashcard-controls">
                            <button class="control-btn btn-next" onclick="startQuiz('${quizType}')">Пройти ещё раз</button>
                        </div>
                        ${errorsHtml}
                    </div>
                </div>
            `;
        }

        // Reference
        function renderReference(filter = 'all') {
            if (!accountsData) return;
            const filtersEl = document.getElementById('filters');
            const sections = new Set();
            Object.values(accountsData.balance).forEach(acc => sections.add(acc.section));
            sections.add('Забалансовые счета');
            filtersEl.innerHTML = `<button class="filter-btn ${filter === 'all' ? 'active' : ''}" onclick="renderReference('all')">Все</button>`;
            sections.forEach(section => {
                filtersEl.innerHTML += `<button class="filter-btn ${filter === section ? 'active' : ''}" onclick="renderReference('${section}')">${section.split('. ')[1] || section}</button>`;
            });
            const listEl = document.getElementById('accountsList');
            listEl.innerHTML = '';
            const allAccounts = {...accountsData.balance, ...accountsData.off_balance};
            Object.entries(allAccounts)
                .filter(([num, acc]) => filter === 'all' || acc.section === filter)
                .sort((a, b) => a[0].localeCompare(b[0], undefined, {numeric: true}))
                .forEach(([number, account]) => {
                    const typeClass = account.type === 'А' ? 'type-active' : account.type === 'П' ? 'type-passive' : account.type ? 'type-mixed' : '';
                    const typeText = account.type === 'А' ? 'А' : account.type === 'П' ? 'П' : account.type === 'А/П' ? 'А/П' : '';
                    listEl.innerHTML += `<div class="account-item"><span class="number">${number}</span><span class="name">${account.name}</span>${typeText ? `<span class="type-badge ${typeClass}">${typeText}</span>` : ''}</div>`;
                });
        }

        // Navigation
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const mode = btn.dataset.mode;
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                document.getElementById(mode).classList.add('active');
                
                if (mode === 'flashcards') loadFlashcard();
                else if (mode.startsWith('quiz-')) startQuiz(mode);
            });
        });

        init();
    </script>
</body>
</html>'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/accounts')
def get_accounts():
    return jsonify({
        "balance": ACCOUNTS,
        "off_balance": OFF_BALANCE_ACCOUNTS
    })


@app.route('/api/quiz/number-to-name')
def quiz_number_to_name():
    all_accounts = {**ACCOUNTS, **OFF_BALANCE_ACCOUNTS}
    correct_number = random.choice(list(all_accounts.keys()))
    correct_account = all_accounts[correct_number]
    wrong_numbers = [n for n in all_accounts.keys() if n != correct_number]
    wrong_numbers = random.sample(wrong_numbers, min(3, len(wrong_numbers)))
    options = [correct_account["name"]]
    for n in wrong_numbers:
        options.append(all_accounts[n]["name"])
    random.shuffle(options)
    return jsonify({
        "question": f"Как называется счёт <strong>{correct_number}</strong>?",
        "number": correct_number,
        "options": options,
        "correct": correct_account["name"],
        "section": correct_account.get("section", "")
    })


@app.route('/api/quiz/name-to-number')
def quiz_name_to_number():
    all_accounts = {**ACCOUNTS, **OFF_BALANCE_ACCOUNTS}
    correct_number = random.choice(list(all_accounts.keys()))
    correct_account = all_accounts[correct_number]
    wrong_numbers = [n for n in all_accounts.keys() if n != correct_number]
    wrong_numbers = random.sample(wrong_numbers, min(3, len(wrong_numbers)))
    options = [correct_number] + wrong_numbers
    random.shuffle(options)
    return jsonify({
        "question": f"Какой номер у счёта \"<strong>{correct_account['name']}</strong>\"?",
        "name": correct_account["name"],
        "options": options,
        "correct": correct_number,
        "section": correct_account.get("section", "")
    })


@app.route('/api/quiz/type')
def quiz_type():
    accounts_with_type = {k: v for k, v in ACCOUNTS.items() if "type" in v}
    correct_number = random.choice(list(accounts_with_type.keys()))
    correct_account = accounts_with_type[correct_number]
    type_full = {"А": "Активный", "П": "Пассивный", "А/П": "Активно-пассивный"}
    options = ["Активный", "Пассивный", "Активно-пассивный"]
    return jsonify({
        "question": f"Какой тип у счёта <strong>{correct_number}</strong> \"{correct_account['name']}\"?",
        "number": correct_number,
        "name": correct_account["name"],
        "options": options,
        "correct": type_full[correct_account["type"]],
        "section": correct_account.get("section", "")
    })


@app.route('/api/quiz/section')
def quiz_section():
    correct_number = random.choice(list(ACCOUNTS.keys()))
    correct_account = ACCOUNTS[correct_number]
    
    # Get all unique sections
    all_sections = list(set(a["section"] for a in ACCOUNTS.values()))
    correct_section = correct_account["section"]
    
    # Get wrong options
    wrong_sections = [s for s in all_sections if s != correct_section]
    wrong_sections = random.sample(wrong_sections, min(3, len(wrong_sections)))
    
    options = [correct_section] + wrong_sections
    random.shuffle(options)
    
    return jsonify({
        "question": f"К какому разделу относится счёт <strong>{correct_number}</strong> \"{correct_account['name']}\"?",
        "number": correct_number,
        "name": correct_account["name"],
        "options": options,
        "correct": correct_section,
        "section": correct_section
    })


@app.route('/api/flashcard')
def flashcard():
    all_accounts = {**ACCOUNTS, **OFF_BALANCE_ACCOUNTS}
    number = random.choice(list(all_accounts.keys()))
    account = all_accounts[number]
    return jsonify({
        "number": number,
        "name": account["name"],
        "section": account.get("section", ""),
        "type": account.get("type", "")
    })


if __name__ == '__main__':
    app.run(debug=True, port=5050)
