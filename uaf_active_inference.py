"""
UAF Active Inference Engine
Максимизирует Normalized Predictive Gain (NPG) через:
1. Минимизацию вариационной свободной энергии на каждом уровне
2. Адаптивную точность (precision) как функцию критичности
3. Active Inference: выбор действий с минимальным Expected Free Energy
4. Иерархическую связку: ошибка вверх, prior вниз

Запуск: python uaf_active_inference.py
Требует: numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. УРОВЕНЬ ПРЕДСКАЗАНИЯ (L_k)
# =============================================================================
class UAFLevel:
    """
    Один уровень иерархии UAF.
    Хранит belief Q(s), prior P(s) от верхнего уровня, precision π.
    Минимизирует F = Surprise + KL(Q||P)
    """
    def __init__(self, name: str, dim: int, precision_init: float = 1.0):
        self.name = name
        self.dim = dim
        self.precision = precision_init          # обратная дисперсия / вес ошибки
        self.belief = np.zeros(dim)              # Q(s) — текущая модель
        self.prior = np.zeros(dim)               # P(s) — ограничение сверху
        self.history = {'belief': [], 'surprise': [], 'free_energy': [], 'npg': []}

    def compute_surprise(self, observation: np.ndarray):
        """S = -log P(o|Q) для гауссовской модели с точностью π"""
        error = observation - self.belief
        surprise = 0.5 * self.precision * np.sum(error**2)
        return surprise, error

    def compute_free_energy(self, surprise: float) -> float:
        """F = S + D_KL(Q||P). Для единичной ковариации KL = 0.5*||Q-P||^2"""
        kl = 0.5 * np.sum((self.belief - self.prior)**2)
        return surprise + kl

    def update_belief(self, error: np.ndarray, dt: float = 0.1):
        """Градиентный спуск по F: dQ/dt = -∂F/∂Q"""
        # ∂F/∂Q = -π*error + (Q - P)
        grad = -self.precision * error + (self.belief - self.prior)
        self.belief -= dt * grad

        # Самоорганизующаяся точность (criticality)
        # Если ошибка растёт → повышаем π (быстрее учимся)
        # Если ошибка мала → снижаем π (стабилизируемся)
        target_error = 0.5
        self.precision = np.clip(
            self.precision + 0.05 * (np.abs(error).mean() - target_error),
            0.1, 5.0
        )

    def record(self, surprise: float, fe: float, npg: float):
        self.history['belief'].append(self.belief.copy())
        self.history['surprise'].append(surprise)
        self.history['free_energy'].append(fe)
        self.history['npg'].append(npg)


# =============================================================================
# 2. ACTIVE INFERENCE АГЕНТ (Выбор действий)
# =============================================================================
class UAFActiveAgent:
    """
    Агент, выбирающий действие с минимальным Expected Free Energy (EFE).
    G(π) = Risk + Ambiguity
    Risk = D_KL(Q(o|a) || P_pref(o))
    Ambiguity = E[H[P(o|s,a)]]
    """
    def __init__(self, actions: list, dim_obs: int):
        self.actions = actions
        self.dim_obs = dim_obs
        # Предпочтения (целевое распределение наблюдений)
        self.preferred_obs = np.zeros(dim_obs)
        # Модели исходов для каждого действия: mean, variance
        self.outcome_models = {
            a: {'mean': np.random.randn(dim_obs)*0.5, 'var': np.ones(dim_obs)*0.8}
            for a in actions
        }

    def compute_efe(self, action: str) -> float:
        """Ожидаемая свободная энергия для действия"""
        model = self.outcome_models[action]
        pred_mean = model['mean']
        pred_var = model['var']

        # Risk: KL между предсказанным исходом и предпочтением
        # Для диагональных гауссиан: KL = 0.5*Σ[(μ-μ_pref)^2/σ^2 + log(σ_pref^2/σ^2) - 1]
        # Упрощаем: σ_pref=1, тогда Risk ≈ 0.5*Σ(μ-μ_pref)^2
        risk = 0.5 * np.sum((pred_mean - self.preferred_obs)**2)

        # Ambiguity: ожидаемая энтропия исхода H = 0.5*log(2πeσ^2)
        ambiguity = 0.5 * np.sum(np.log(2 * np.pi * np.e * pred_var))

        return risk + ambiguity

    def select_action(self) -> str:
        """Выбираем действие с минимальным EFE"""
        efes = {a: self.compute_efe(a) for a in self.actions}
        best = min(efes, key=efes.get)
        return best, efes

    def update_outcome_model(self, action: str, actual_obs: np.ndarray, lr: float = 0.1):
        """Обновляем модель исхода после наблюдения (байесовское усреднение)"""
        model = self.outcome_models[action]
        model['mean'] = (1 - lr) * model['mean'] + lr * actual_obs
        model['var'] = np.clip(
            (1 - lr) * model['var'] + lr * (actual_obs - model['mean'])**2,
            0.1, 2.0
        )


# =============================================================================
# 3. СРЕДА (Генератор наблюдений)
# =============================================================================
class Environment:
    """
    Простая нестационарная среда.
    Наблюдение = скрытое состояние + шум.
    Скрытое состояние дрейфует + реагирует на действие агента.
    """
    def __init__(self, dim: int):
        self.dim = dim
        self.state = np.zeros(dim)
        self.drift = np.random.randn(dim) * 0.02

    def step(self, action: str) -> np.ndarray:
        # Действие влияет на среду (упрощённо)
        action_effect = {
            'explore': np.random.randn(self.dim) * 0.3,
            'exploit': np.zeros(self.dim),
            'wait': np.zeros(self.dim)
        }.get(action, np.zeros(self.dim))

        # Дрейф + действие + шум
        self.state += self.drift + action_effect + np.random.randn(self.dim) * 0.1
        observation = self.state + np.random.randn(self.dim) * 0.2
        return observation


# =============================================================================
# 4. СИСТЕМА UAF (Сборка и цикл)
# =============================================================================
class UAFSystem:
    def __init__(self, level_configs: list, actions: list, dim: int):
        self.levels = [UAFLevel(**cfg) for cfg in level_configs]
        self.agent = UAFActiveAgent(actions, dim)
        self.env = Environment(dim)
        self.baseline_fe = 1.0  # Для расчёта NPG
        self.time = 0

    def step(self):
        self.time += 1

        # 1. Агент выбирает действие через Active Inference
        action, efes = self.agent.select_action()

        # 2. Среда генерирует наблюдение
        obs = self.env.step(action)

        # 3. Bottom-up: вычисляем surprise и ошибку на каждом уровне
        errors = []
        surprises = []
        current_obs = obs
        for level in self.levels:
            s, e = level.compute_surprise(current_obs)
            surprises.append(s)
            errors.append(e)
            current_obs = e  # Ошибка передаётся вверх

        # 4. Top-down: priors от верхних уровней
        for i in range(len(self.levels) - 1, 0, -1):
            self.levels[i - 1].prior = self.levels[i].belief.copy()

        # 5. Обновление убеждений и расчёт метрик
        npgs = []
        for i, level in enumerate(self.levels):
            fe = level.compute_free_energy(surprises[i])
            level.update_belief(errors[i])

            # NPG = (baseline - current_F) / baseline
            npg = (self.baseline_fe - fe) / self.baseline_fe
            npg = np.clip(npg, -3.0, 3.0)
            npgs.append(npg)
            level.record(surprises[i], fe, npg)

        # 6. Обновляем модель исходов агента
        self.agent.update_outcome_model(action, obs)

        # Адаптируем baseline по мере обучения (экспоненциальное сглаживание)
        avg_fe = np.mean([level.history['free_energy'][-1] for level in self.levels])
        self.baseline_fe = 0.95 * self.baseline_fe + 0.05 * max(avg_fe, 0.1)

        return action, npgs, efes

    def run(self, steps: int):
        log = {'action': [], 'npg': [], 'efe': []}
        for _ in range(steps):
            action, npgs, efes = self.step()
            log['action'].append(action)
            log['npg'].append(npgs)
            log['efe'].append(efes)
        return log


# =============================================================================
# 5. ВИЗУАЛИЗАЦИЯ
# =============================================================================
def plot_results(log, levels):
    steps = len(log['npg'])
    t = np.arange(steps)

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # NPG по уровням
    npg_array = np.array(log['npg'])
    for i, level in enumerate(levels):
        axes[0].plot(t, npg_array[:, i], label=f"{level.name} NPG", linewidth=2)
    axes[0].axhline(0, color='gray', linestyle='--')
    axes[0].set_ylabel("NPG (Normalized Predictive Gain)")
    axes[0].set_title("UAF: Максимизация NPG через минимизацию Free Energy")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Действия агента
    action_map = {'explore': 0, 'exploit': 1, 'wait': 2}
    actions_num = [action_map[a] for a in log['action']]
    axes[1].scatter(t, actions_num, c=actions_num, cmap='viridis', s=15, alpha=0.7)
    axes[1].set_yticks([0, 1, 2])
    axes[1].set_yticklabels(['explore', 'exploit', 'wait'])
    axes[1].set_ylabel("Active Inference Action")
    axes[1].grid(True, alpha=0.3)

    # Средняя Free Energy
    avg_fe = []
    for i in range(steps):
        fes = [levels[j].history['free_energy'][i] for j in range(len(levels))]
        avg_fe.append(np.mean(fes))
    axes[2].plot(t, avg_fe, color='crimson', linewidth=2)
    axes[2].set_ylabel("Mean Free Energy")
    axes[2].set_xlabel("Time Steps")
    axes[2].set_title("Снижение F → Рост NPG")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# =============================================================================
# 6. ЗАПУСК
# =============================================================================
if __name__ == "__main__":
    # Конфигурация уровней
    level_configs = [
        {"name": "L0_Sensory",   "dim": 4, "precision_init": 2.0},
        {"name": "L1_Cognitive", "dim": 4, "precision_init": 1.0},
        {"name": "L2_Social",    "dim": 4, "precision_init": 0.5},
    ]

    actions = ['explore', 'exploit', 'wait']
    dim_obs = 4

    system = UAFSystem(level_configs, actions, dim_obs)
    print("▶ Запуск UAF Active Inference Engine...")
    print("  Цель: максимизация NPG через минимизацию Free Energy")
    print("  Механизмы: hierarchical coupling, adaptive precision, EFE selection\n")

    log = system.run(steps=500)

    # Финальная статистика
    final_npg = np.mean([level.history['npg'][-50:] for level in system.levels])
    print(f"✓ Завершено. Средний NPG (последние 50 шагов): {final_npg:.3f}")
    print("  NPG > 0 → система предсказывает лучше baseline")
    print("  NPG → +1 → оптимальное сжатие surprise\n")

    plot_results(log, system.levels)
