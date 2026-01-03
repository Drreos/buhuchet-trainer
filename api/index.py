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
            --text-primary: #ffffff;
            --text-secondary: #8892a6;
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #00f5d4 0%, #00bbf9 100%);
            --gradient-3: linear-gradient(135deg, #f72585 0%, #7209b7 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Unbounded', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 245, 212, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(247, 37, 133, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(76, 201, 240, 0.05) 0%, transparent 40%);
        }

        .bg-animation::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 50px 50px;
        }

        header {
            padding: 2rem;
            text-align: center;
            position: relative;
        }

        .logo {
            font-size: 2.5rem;
            font-weight: 800;
            background: var(--gradient-2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 300;
            letter-spacing: 2px;
        }

        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 3rem;
            padding: 1rem;
            margin: 1rem auto;
            max-width: 600px;
        }

        .stat {
            text-align: center;
        }

        .stat-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem;
            font-weight: 600;
            color: var(--accent-cyan);
        }

        .stat-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .mode-nav {
            display: flex;
            justify-content: center;
            gap: 1rem;
            padding: 1rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }

        .mode-btn {
            padding: 0.8rem 1.5rem;
            border: 2px solid transparent;
            background: var(--bg-card);
            color: var(--text-secondary);
            font-family: 'Unbounded', sans-serif;
            font-size: 0.8rem;
            font-weight: 400;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .mode-btn:hover {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 245, 212, 0.2);
        }

        .mode-btn.active {
            background: var(--gradient-2);
            color: var(--bg-primary);
            border-color: transparent;
            font-weight: 600;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 2rem 4rem;
        }

        .card {
            background: var(--bg-card);
            border-radius: 24px;
            padding: 3rem;
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.5s ease;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-2);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .flashcard-container {
            perspective: 1000px;
            min-height: 350px;
        }

        .flashcard {
            width: 100%;
            height: 350px;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }

        .flashcard.flipped {
            transform: rotateY(180deg);
        }

        .flashcard-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 24px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .flashcard-front {
            background: linear-gradient(145deg, var(--bg-card), #243050);
            border: 2px solid rgba(0, 245, 212, 0.2);
        }

        .flashcard-back {
            background: linear-gradient(145deg, #1a3a4a, var(--bg-card));
            border: 2px solid rgba(247, 37, 133, 0.2);
            transform: rotateY(180deg);
        }

        .account-number {
            font-family: 'JetBrains Mono', monospace;
            font-size: 6rem;
            font-weight: 600;
            background: var(--gradient-2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
        }

        .account-hint {
            color: var(--text-secondary);
            font-size: 0.8rem;
            margin-top: 2rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .account-name {
            font-size: 1.8rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 1rem;
            background: var(--gradient-3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .account-section {
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-align: center;
        }

        .account-type {
            margin-top: 1rem;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .type-active { background: rgba(0, 245, 212, 0.2); color: var(--accent-cyan); }
        .type-passive { background: rgba(247, 37, 133, 0.2); color: var(--accent-magenta); }
        .type-mixed { background: rgba(254, 228, 64, 0.2); color: var(--accent-yellow); }

        .flashcard-controls {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }

        .control-btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-family: 'Unbounded', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn-next {
            background: var(--gradient-2);
            color: var(--bg-primary);
        }

        .btn-next:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 40px rgba(0, 245, 212, 0.3);
        }

        .quiz-question {
            font-size: 1.4rem;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 300;
            line-height: 1.6;
        }

        .quiz-question strong {
            font-weight: 600;
            color: var(--accent-cyan);
        }

        .quiz-options {
            display: grid;
            gap: 1rem;
        }

        .quiz-option {
            padding: 1.2rem 1.5rem;
            background: var(--bg-secondary);
            border: 2px solid transparent;
            border-radius: 16px;
            font-family: 'Unbounded', sans-serif;
            font-size: 1rem;
            color: var(--text-primary);
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
        }

        .quiz-option:hover:not(.disabled) {
            border-color: var(--accent-cyan);
            background: rgba(0, 245, 212, 0.1);
            transform: translateX(10px);
        }

        .quiz-option.correct {
            border-color: var(--accent-cyan);
            background: rgba(0, 245, 212, 0.2);
        }

        .quiz-option.wrong {
            border-color: var(--accent-magenta);
            background: rgba(247, 37, 133, 0.2);
        }

        .quiz-option.disabled {
            cursor: default;
            opacity: 0.7;
        }

        .quiz-feedback {
            text-align: center;
            margin-top: 2rem;
            padding: 1.5rem;
            border-radius: 16px;
            animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .quiz-feedback.success {
            background: rgba(0, 245, 212, 0.1);
            border: 1px solid rgba(0, 245, 212, 0.3);
        }

        .quiz-feedback.error {
            background: rgba(247, 37, 133, 0.1);
            border: 1px solid rgba(247, 37, 133, 0.3);
        }

        .quiz-feedback h3 {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }

        .quiz-feedback.success h3 { color: var(--accent-cyan); }
        .quiz-feedback.error h3 { color: var(--accent-magenta); }

        .quiz-feedback p {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .reference-filters {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }

        .filter-btn {
            padding: 0.6rem 1.2rem;
            border: 1px solid var(--text-secondary);
            background: transparent;
            color: var(--text-secondary);
            font-family: 'Unbounded', sans-serif;
            font-size: 0.7rem;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s ease;
        }

        .filter-btn:hover, .filter-btn.active {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }

        .accounts-list {
            display: grid;
            gap: 0.8rem;
        }

        .account-item {
            display: flex;
            align-items: center;
            padding: 1rem 1.5rem;
            background: var(--bg-secondary);
            border-radius: 12px;
            transition: all 0.3s ease;
        }

        .account-item:hover {
            background: rgba(0, 245, 212, 0.1);
            transform: translateX(5px);
        }

        .account-item .number {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--accent-cyan);
            min-width: 60px;
        }

        .account-item .name {
            flex: 1;
            font-size: 0.95rem;
        }

        .account-item .type-badge {
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
        }

        .section { display: none; }
        .section.active { display: block; }

        @media (max-width: 600px) {
            .logo { font-size: 1.8rem; }
            .stats-bar { gap: 1.5rem; }
            .stat-value { font-size: 1.5rem; }
            .mode-btn { padding: 0.6rem 1rem; font-size: 0.7rem; }
            .card { padding: 1.5rem; }
            .account-number { font-size: 4rem; }
            .quiz-question { font-size: 1.1rem; }
        }

        .progress-ring {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 80px;
            height: 80px;
        }

        .progress-ring circle {
            fill: none;
            stroke-width: 6;
        }

        .progress-ring .bg {
            stroke: var(--bg-card);
        }

        .progress-ring .progress {
            stroke: url(#progressGradient);
            stroke-linecap: round;
            transform: rotate(-90deg);
            transform-origin: center;
            transition: stroke-dashoffset 0.5s ease;
        }

        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--accent-cyan);
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <header>
        <h1 class="logo">Бухучёт</h1>
        <p class="subtitle">Тренажёр плана счетов</p>
    </header>

    <div class="stats-bar">
        <div class="stat">
            <div class="stat-value" id="correctCount">0</div>
            <div class="stat-label">Верно</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="totalCount">0</div>
            <div class="stat-label">Всего</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="streakCount">0</div>
            <div class="stat-label">Серия</div>
        </div>
    </div>

    <nav class="mode-nav">
        <button class="mode-btn active" data-mode="flashcards">Карточки</button>
        <button class="mode-btn" data-mode="quiz-number">Номер → Название</button>
        <button class="mode-btn" data-mode="quiz-name">Название → Номер</button>
        <button class="mode-btn" data-mode="quiz-type">Тип счёта</button>
        <button class="mode-btn" data-mode="reference">Справочник</button>
    </nav>

    <div class="container">
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
                <button class="control-btn btn-next" onclick="nextFlashcard()">Следующая карточка →</button>
            </div>
        </section>

        <section id="quiz-number" class="section">
            <div class="card">
                <div class="quiz-question" id="quizNumberQuestion">
                    Как называется счёт <strong>01</strong>?
                </div>
                <div class="quiz-options" id="quizNumberOptions"></div>
                <div class="quiz-feedback" id="quizNumberFeedback" style="display: none;"></div>
                <div class="flashcard-controls">
                    <button class="control-btn btn-next" onclick="loadQuizNumber()" style="display: none;" id="quizNumberNext">Следующий вопрос →</button>
                </div>
            </div>
        </section>

        <section id="quiz-name" class="section">
            <div class="card">
                <div class="quiz-question" id="quizNameQuestion">
                    Какой номер у счёта "Основные средства"?
                </div>
                <div class="quiz-options" id="quizNameOptions"></div>
                <div class="quiz-feedback" id="quizNameFeedback" style="display: none;"></div>
                <div class="flashcard-controls">
                    <button class="control-btn btn-next" onclick="loadQuizName()" style="display: none;" id="quizNameNext">Следующий вопрос →</button>
                </div>
            </div>
        </section>

        <section id="quiz-type" class="section">
            <div class="card">
                <div class="quiz-question" id="quizTypeQuestion">
                    Какой тип у счёта <strong>01</strong> "Основные средства"?
                </div>
                <div class="quiz-options" id="quizTypeOptions"></div>
                <div class="quiz-feedback" id="quizTypeFeedback" style="display: none;"></div>
                <div class="flashcard-controls">
                    <button class="control-btn btn-next" onclick="loadQuizType()" style="display: none;" id="quizTypeNext">Следующий вопрос →</button>
                </div>
            </div>
        </section>

        <section id="reference" class="section">
            <div class="card">
                <div class="reference-filters" id="filters"></div>
                <div class="accounts-list" id="accountsList"></div>
            </div>
        </section>
    </div>

    <div class="progress-ring">
        <svg viewBox="0 0 80 80">
            <defs>
                <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#00f5d4"/>
                    <stop offset="100%" stop-color="#00bbf9"/>
                </linearGradient>
            </defs>
            <circle class="bg" cx="40" cy="40" r="34"/>
            <circle class="progress" cx="40" cy="40" r="34" 
                    stroke-dasharray="213.6" 
                    stroke-dashoffset="213.6"
                    id="progressCircle"/>
        </svg>
        <div class="progress-text" id="progressPercent">0%</div>
    </div>

    <script>
        let stats = { correct: 0, total: 0, streak: 0, maxStreak: 0 };
        let accountsData = null;
        let currentQuiz = null;

        async function init() {
            const response = await fetch('/api/accounts');
            accountsData = await response.json();
            loadFlashcard();
            renderReference();
        }

        function updateStats(correct) {
            if (correct) {
                stats.correct++;
                stats.streak++;
                if (stats.streak > stats.maxStreak) stats.maxStreak = stats.streak;
            } else {
                stats.streak = 0;
            }
            stats.total++;
            document.getElementById('correctCount').textContent = stats.correct;
            document.getElementById('totalCount').textContent = stats.total;
            document.getElementById('streakCount').textContent = stats.streak;
            const percent = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;
            const circumference = 2 * Math.PI * 34;
            const offset = circumference - (percent / 100) * circumference;
            document.getElementById('progressCircle').style.strokeDashoffset = offset;
            document.getElementById('progressPercent').textContent = percent + '%';
        }

        function flipCard() {
            document.getElementById('flashcard').classList.toggle('flipped');
        }

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
                } else {
                    typeEl.style.display = 'none';
                }
            }, 100);
        }

        function nextFlashcard() { loadFlashcard(); }

        async function loadQuizNumber() {
            const response = await fetch('/api/quiz/number-to-name');
            currentQuiz = await response.json();
            document.getElementById('quizNumberQuestion').innerHTML = `Как называется счёт <strong>${currentQuiz.number}</strong>?`;
            const optionsEl = document.getElementById('quizNumberOptions');
            optionsEl.innerHTML = '';
            currentQuiz.options.forEach(option => {
                const btn = document.createElement('button');
                btn.className = 'quiz-option';
                btn.textContent = option;
                btn.onclick = () => checkAnswer('number', option, btn);
                optionsEl.appendChild(btn);
            });
            document.getElementById('quizNumberFeedback').style.display = 'none';
            document.getElementById('quizNumberNext').style.display = 'none';
        }

        async function loadQuizName() {
            const response = await fetch('/api/quiz/name-to-number');
            currentQuiz = await response.json();
            document.getElementById('quizNameQuestion').innerHTML = `Какой номер у счёта "<strong>${currentQuiz.name}</strong>"?`;
            const optionsEl = document.getElementById('quizNameOptions');
            optionsEl.innerHTML = '';
            currentQuiz.options.forEach(option => {
                const btn = document.createElement('button');
                btn.className = 'quiz-option';
                btn.textContent = option;
                btn.onclick = () => checkAnswer('name', option, btn);
                optionsEl.appendChild(btn);
            });
            document.getElementById('quizNameFeedback').style.display = 'none';
            document.getElementById('quizNameNext').style.display = 'none';
        }

        async function loadQuizType() {
            const response = await fetch('/api/quiz/type');
            currentQuiz = await response.json();
            document.getElementById('quizTypeQuestion').innerHTML = `Какой тип у счёта <strong>${currentQuiz.number}</strong> "${currentQuiz.name}"?`;
            const optionsEl = document.getElementById('quizTypeOptions');
            optionsEl.innerHTML = '';
            currentQuiz.options.forEach(option => {
                const btn = document.createElement('button');
                btn.className = 'quiz-option';
                btn.textContent = option;
                btn.onclick = () => checkAnswer('type', option, btn);
                optionsEl.appendChild(btn);
            });
            document.getElementById('quizTypeFeedback').style.display = 'none';
            document.getElementById('quizTypeNext').style.display = 'none';
        }

        function checkAnswer(quizType, answer, btnEl) {
            const isCorrect = answer === currentQuiz.correct;
            const feedbackEl = document.getElementById(`quiz${capitalize(quizType)}Feedback`);
            const nextBtn = document.getElementById(`quiz${capitalize(quizType)}Next`);
            document.querySelectorAll(`#quiz${capitalize(quizType)}Options .quiz-option`).forEach(btn => {
                btn.classList.add('disabled');
                if (btn.textContent === currentQuiz.correct) btn.classList.add('correct');
            });
            if (!isCorrect) btnEl.classList.add('wrong');
            feedbackEl.style.display = 'block';
            if (isCorrect) {
                feedbackEl.className = 'quiz-feedback success';
                feedbackEl.innerHTML = `<h3>✓ Верно!</h3><p>${currentQuiz.section || ''}</p>`;
            } else {
                feedbackEl.className = 'quiz-feedback error';
                feedbackEl.innerHTML = `<h3>✗ Неверно</h3><p>Правильный ответ: <strong>${currentQuiz.correct}</strong></p><p>${currentQuiz.section || ''}</p>`;
            }
            nextBtn.style.display = 'inline-block';
            updateStats(isCorrect);
        }

        function capitalize(str) { return str.charAt(0).toUpperCase() + str.slice(1); }

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

        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const mode = btn.dataset.mode;
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                document.getElementById(mode).classList.add('active');
                if (mode === 'quiz-number') loadQuizNumber();
                else if (mode === 'quiz-name') loadQuizName();
                else if (mode === 'quiz-type') loadQuizType();
                else if (mode === 'flashcards') loadFlashcard();
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
        "question": f"Как называется счёт {correct_number}?",
        "number": correct_number,
        "options": options,
        "correct": correct_account["name"],
        "section": correct_account.get("section", ""),
        "type": correct_account.get("type", "")
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
        "question": f"Какой номер у счёта \"{correct_account['name']}\"?",
        "name": correct_account["name"],
        "options": options,
        "correct": correct_number,
        "section": correct_account.get("section", ""),
        "type": correct_account.get("type", "")
    })


@app.route('/api/quiz/type')
def quiz_type():
    accounts_with_type = {k: v for k, v in ACCOUNTS.items() if "type" in v}
    correct_number = random.choice(list(accounts_with_type.keys()))
    correct_account = accounts_with_type[correct_number]
    type_full = {"А": "Активный", "П": "Пассивный", "А/П": "Активно-пассивный"}
    options = ["Активный", "Пассивный", "Активно-пассивный"]
    return jsonify({
        "question": f"Какой тип у счёта {correct_number} \"{correct_account['name']}\"?",
        "number": correct_number,
        "name": correct_account["name"],
        "options": options,
        "correct": type_full[correct_account["type"]],
        "section": correct_account.get("section", "")
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

