import sys
import re

file_path = r"C:\Users\anali\.gemini\antigravity\scratch\dashboard-treino\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS
css_to_add = """
        .set-counter { cursor: pointer; transition: background 0.2s; user-select: none; }
        .set-counter:hover { background: #cbd5e1; }
        .set-counter.done { background: var(--success) !important; color: white !important; border: none; }
        .swap-btn { background: #e2e8f0; color: #475569; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 0.8em; margin-left: 5px; }
        .swap-btn:hover { background: #cbd5e1; }
        .add-ex-btn { display: block; width: 100%; text-align: center; background: transparent; border: 2px dashed #cbd5e1; color: var(--secondary); padding: 10px; border-radius: 8px; cursor: pointer; font-weight: bold; margin-top: 10px; transition: all 0.2s; }
        .add-ex-btn:hover { background: #f8fafc; border-color: var(--primary); color: var(--primary); }

        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: none; align-items: center; justify-content: center; z-index: 2000; padding: 20px; }
        .modal-overlay.active { display: flex; }
        .modal-content { background: white; padding: 20px; border-radius: 12px; width: 100%; max-width: 400px; max-height: 80vh; overflow-y: auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .modal-content h3 { margin-top: 0; color: var(--dark); border-bottom: 1px solid #e2e8f0; padding-bottom: 10px; }
        .modal-btn { display: block; width: 100%; padding: 12px; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 10px; cursor: pointer; text-align: left; font-size: 1em; transition: all 0.2s; }
        .modal-btn:hover { background: #e0f2fe; border-color: #7dd3fc; }
        .modal-btn strong { display: block; color: var(--primary); margin-bottom: 3px; }
        .modal-close { background: var(--danger); color: white; text-align: center; justify-content: center; border: none; margin-top: 10px; font-weight: bold; }
    </style>
"""
content = content.replace("    </style>", css_to_add)

# 2. Add Modal HTML before timer-bar
modal_html = """
    <!-- Modal de Troca/Adição -->
    <div id="swapModal" class="modal-overlay" onclick="closeSwapModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <h3 id="modalTitle">🔄 Selecione a Opção</h3>
            <div id="modalList"></div>
            <button class="modal-btn modal-close" onclick="closeSwapModal()">Cancelar</button>
        </div>
    </div>

    <!-- TEMPORIZADOR FIXO -->
"""
content = content.replace("    <!-- TEMPORIZADOR FIXO -->", modal_html)


# 3. Replace TERÇA to SEXTA
new_workouts_html = """    <!-- TERÇA -->
    <div id="terca" class="workout-card active">
        <h2>💪 Terça - Peito, Ombro e Tríceps <span class="calories-tag">🔥 Gasto: ~300 kcal</span></h2>
        <ul class="exercise-list">
            <li class="exercise-item" id="t1" onclick="toggleExercise('t1', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Svend Press em Pé com Anilha/Halter <button class="swap-btn" onclick="openSwapModal('t1', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">10 a 12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_t1" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('t1', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=svend+press+com+anilha+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="t2" onclick="toggleExercise('t2', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Desenvolvimento de Ombros em Pé <button class="swap-btn" onclick="openSwapModal('t2', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">10 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_t2" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('t2', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=desenvolvimento+com+halter+em+pe" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="t3" onclick="toggleExercise('t3', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Elevação Lateral <button class="swap-btn" onclick="openSwapModal('t3', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 a 15 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_t3" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('t3', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=eleva%C3%A7%C3%A3o+lateral+halteres" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="t4" onclick="toggleExercise('t4', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Tríceps Francês em Pé com Halter <button class="swap-btn" onclick="openSwapModal('t4', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_t4" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('t4', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=triceps+frances+com+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="t5" onclick="toggleExercise('t5', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Tríceps Coice com Halter <button class="swap-btn" onclick="openSwapModal('t5', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 a 15 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_t5" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('t5', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=triceps+coice+com+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="t6" onclick="toggleExercise('t6', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Crucifixo Invertido com Halteres <button class="swap-btn" onclick="openSwapModal('t6', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_t6" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('t6', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=crucifixo+invertido+com+halteres" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
        </ul>
        <button class="add-ex-btn" onclick="openAddModal('terca')">➕ Adicionar Exercício Manual</button>
        <div class="action-area"><button class="save-btn" onclick="saveProgressToday('Terça')">☁️ Salvar Treino de Hoje</button></div>
    </div>

    <!-- QUARTA -->
    <div id="quarta" class="workout-card">
        <h2>🦵 Quarta - Pernas e Glúteos <span class="calories-tag">🔥 Gasto: ~400 kcal</span></h2>
        <ul class="exercise-list">
            <li class="exercise-item" id="q1" onclick="toggleExercise('q1', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Agachamento Livre com Halteres (Goblet) <button class="swap-btn" onclick="openSwapModal('q1', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_q1" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('q1', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=agachamento+goblet" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="q2" onclick="toggleExercise('q2', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Agachamento Búlgaro com Taça <button class="swap-btn" onclick="openSwapModal('q2', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">10 cada perna</span>
                        <div class="weight-control">
                            <input type="number" id="carga_q2" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('q2', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=agachamento+bulgaro" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="q3" onclick="toggleExercise('q3', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Stiff com Halter ou Barra <button class="swap-btn" onclick="openSwapModal('q3', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">10 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_q3" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('q3', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=stiff+com+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="q4" onclick="toggleExercise('q4', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Gêmeos em Pé com Halteres <button class="swap-btn" onclick="openSwapModal('q4', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">20 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_q4" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('q4', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=panturrilha+em+pe+com+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="q5" onclick="toggleExercise('q5', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Good Morning (Bom Dia) com Barra <button class="swap-btn" onclick="openSwapModal('q5', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_q5" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('q5', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=good+morning+exercicio" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
        </ul>
        <button class="add-ex-btn" onclick="openAddModal('quarta')">➕ Adicionar Exercício Manual</button>
        <div class="action-area"><button class="save-btn" onclick="saveProgressToday('Quarta')">☁️ Salvar Treino de Hoje</button></div>
    </div>

    <!-- QUINTA -->
    <div id="quinta" class="workout-card">
        <h2>💪 Quinta - Costas e Bíceps <span class="calories-tag">🔥 Gasto: ~300 kcal</span></h2>
        <ul class="exercise-list">
            <li class="exercise-item" id="qui1" onclick="toggleExercise('qui1', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Remada Curvada <button class="swap-btn" onclick="openSwapModal('qui1', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">10 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_qui1" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('qui1', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=remada+curvada+com+barra" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="qui2" onclick="toggleExercise('qui2', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Remada Unilateral (Serrote) <button class="swap-btn" onclick="openSwapModal('qui2', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_qui2" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('qui2', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=remada+unilateral+serrote" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="qui3" onclick="toggleExercise('qui3', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Crucifixo Invertido com Halteres <button class="swap-btn" onclick="openSwapModal('qui3', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_qui3" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('qui3', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=crucifixo+invertido+com+halteres" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="qui4" onclick="toggleExercise('qui4', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Rosca Direta com Barra ou Halteres <button class="swap-btn" onclick="openSwapModal('qui4', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_qui4" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('qui4', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=rosca+direta+com+barra" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="qui5" onclick="toggleExercise('qui5', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Rosca Martelo com Halteres <button class="swap-btn" onclick="openSwapModal('qui5', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">12 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_qui5" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('qui5', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=rosca+martelo+com+halteres" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="qui6" onclick="toggleExercise('qui6', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Lenhador (Woodchopper) em Pé com Halter <button class="swap-btn" onclick="openSwapModal('qui6', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">15 cada lado</span>
                        <div class="weight-control">
                            <input type="number" id="carga_qui6" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('qui6', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=woodchopper+com+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
        </ul>
        <button class="add-ex-btn" onclick="openAddModal('quinta')">➕ Adicionar Exercício Manual</button>
        <div class="action-area"><button class="save-btn" onclick="saveProgressToday('Quinta')">☁️ Salvar Treino de Hoje</button></div>
    </div>

    <!-- SEXTA -->
    <div id="sexta" class="workout-card">
        <h2>🔥 Sexta - Queima Calórica Completa <span class="calories-tag">🔥 Gasto: ~450 kcal</span></h2>
        <ul class="exercise-list">
            <li class="exercise-item" id="s1" onclick="toggleExercise('s1', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Levantamento Terra <button class="swap-btn" onclick="openSwapModal('s1', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 4, event)">0 / 4 Séries</span><span class="tag">8 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_s1" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('s1', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=levantamento+terra+barra" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="s2" onclick="toggleExercise('s2', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Thrusters <button class="swap-btn" onclick="openSwapModal('s2', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">10 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_s2" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('s2', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=thruster+com+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="s3" onclick="toggleExercise('s3', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Caminhada do Fazendeiro (Farmer's Walk) <button class="swap-btn" onclick="openSwapModal('s3', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">45 seg</span>
                        <div class="weight-control">
                            <input type="number" id="carga_s3" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('s3', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=farmers+walk+halteres" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="s4" onclick="toggleExercise('s4', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Swing com Halter <button class="swap-btn" onclick="openSwapModal('s4', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">15 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_s4" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('s4', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=kettlebell+swing+com+halter" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
            <li class="exercise-item" id="s5" onclick="toggleExercise('s5', event)">
                <div class="checkbox-container"><input type="checkbox"></div>
                <div class="exercise-details">
                    <div class="exercise-name">Clean and Press com Halteres <button class="swap-btn" onclick="openSwapModal('s5', event)">🔄 Trocar</button></div>
                    <div class="exercise-meta">
                        <span class="tag set-counter" data-current="0" onclick="incrementSet(this, 3, event)">0 / 3 Séries</span><span class="tag">10 Reps</span>
                        <div class="weight-control">
                            <input type="number" id="carga_s5" placeholder="--" onclick="event.stopPropagation()"><span>kg</span>
                            <button class="save-weight-btn" onclick="saveWeight('s5', event)">Salvar</button>
                        </div>
                    </div>
                </div>
                <a href="https://www.youtube.com/results?search_query=clean+and+press+com+halteres" target="_blank" class="video-btn">▶ Vídeo</a>
            </li>
        </ul>
        <button class="add-ex-btn" onclick="openAddModal('sexta')">➕ Adicionar Exercício Manual</button>
        <div class="action-area"><button class="save-btn" onclick="saveProgressToday('Sexta')">☁️ Salvar Treino de Hoje</button></div>
    </div>

    <!-- ABA NUTRIÇÃO E RECEITAS -->"""

pattern = re.compile(r"    <!-- TERÇA -->.*?    <!-- ABA NUTRIÇÃO E RECEITAS -->", re.DOTALL)
content = pattern.sub(new_workouts_html, content)


# 4. Add JavaScript Logic
js_to_add = """
    // --- LÓGICA DE TROCA E CONTADOR DE SÉRIES ---
    const UPSERT_HEADERS = { ...HEADERS, "Prefer": "return=representation, resolution=merge-duplicates" };

    const EXERCISE_DB = {
        "peito": [
            { nome: "Svend Press em Pé", series: 4, reps: "10 a 12 Reps", yt: "svend+press+com+anilha+halter" },
            { nome: "Flexão de Braço (Parede/Joelho)", series: 3, reps: "Até falhar", yt: "flexao+de+braco+para+iniciantes" },
            { nome: "Supino Reto com Halteres (No Chão)", series: 4, reps: "10 a 12 Reps", yt: "floor+press+com+halteres" }
        ],
        "ombro": [
            { nome: "Desenvolvimento em Pé", series: 4, reps: "10 Reps", yt: "desenvolvimento+com+halter+em+pe" },
            { nome: "Elevação Lateral", series: 3, reps: "12 a 15 Reps", yt: "elevação+lateral+halteres" },
            { nome: "Elevação Frontal", series: 3, reps: "12 Reps", yt: "elevacao+frontal+com+halteres" },
            { nome: "Crucifixo Invertido com Halteres", series: 3, reps: "12 Reps", yt: "crucifixo+invertido+com+halteres" }
        ],
        "triceps": [
            { nome: "Tríceps Francês em Pé", series: 3, reps: "12 Reps", yt: "triceps+frances+com+halter" },
            { nome: "Tríceps Coice com Halter", series: 3, reps: "12 a 15 Reps", yt: "triceps+coice+com+halter" },
            { nome: "Mergulho (no banco/cadeira)", series: 3, reps: "Falha", yt: "triceps+mergulho+cadeira" }
        ],
        "pernas": [
            { nome: "Agachamento Livre com Halteres", series: 4, reps: "12 Reps", yt: "agachamento+goblet" },
            { nome: "Agachamento Búlgaro", series: 3, reps: "10 cada perna", yt: "agachamento+bulgaro" },
            { nome: "Stiff com Halter/Barra", series: 4, reps: "10 Reps", yt: "stiff+com+halter" },
            { nome: "Good Morning com Barra", series: 3, reps: "12 Reps", yt: "good+morning+exercicio" },
            { nome: "Avanço / Passada", series: 3, reps: "10 Passos", yt: "passada+com+halter" },
            { nome: "Afundo no lugar", series: 3, reps: "10 cada perna", yt: "afundo+com+halter" }
        ],
        "costas": [
            { nome: "Remada Curvada", series: 4, reps: "10 Reps", yt: "remada+curvada+com+barra" },
            { nome: "Remada Unilateral (Serrote)", series: 3, reps: "12 Reps", yt: "remada+unilateral+serrote" },
            { nome: "Remada Alta", series: 3, reps: "12 Reps", yt: "remada+alta+com+barra" }
        ],
        "biceps": [
            { nome: "Rosca Direta com Barra ou Halteres", series: 4, reps: "12 Reps", yt: "rosca+direta+com+barra" },
            { nome: "Rosca Martelo com Halteres", series: 3, reps: "12 Reps", yt: "rosca+martelo+com+halteres" },
            { nome: "Rosca Concentrada", series: 3, reps: "10 Reps", yt: "rosca+concentrada" }
        ],
        "core_full": [
            { nome: "Lenhador (Woodchopper) em Pé", series: 3, reps: "15 cada lado", yt: "woodchopper+com+halter" },
            { nome: "Abdominal Clássico no Chão", series: 4, reps: "15 Reps", yt: "abdominal+supra" },
            { nome: "Levantamento Terra", series: 4, reps: "8 Reps", yt: "levantamento+terra+barra" },
            { nome: "Thrusters", series: 3, reps: "10 Reps", yt: "thruster+com+halter" },
            { nome: "Caminhada do Fazendeiro", series: 3, reps: "45 seg", yt: "farmers+walk+halteres" },
            { nome: "Swing com Halter", series: 3, reps: "15 Reps", yt: "kettlebell+swing+com+halter" },
            { nome: "Clean and Press", series: 3, reps: "10 Reps", yt: "clean+and+press+com+halteres" }
        ]
    };

    const SLOT_CATEGORY = {
        "t1": "peito", "t2": "ombro", "t3": "ombro", "t4": "triceps", "t5": "triceps", "t6": "ombro",
        "q1": "pernas", "q2": "pernas", "q3": "pernas", "q4": "pernas", "q5": "pernas",
        "qui1": "costas", "qui2": "costas", "qui3": "ombro", "qui4": "biceps", "qui5": "biceps", "qui6": "core_full",
        "s1": "core_full", "s2": "core_full", "s3": "core_full", "s4": "core_full", "s5": "core_full"
    };

    let currentSwapSlotId = null;

    function incrementSet(el, maxSets, event) {
        event.stopPropagation();
        let current = parseInt(el.getAttribute('data-current') || '0');
        current++;
        if (current > maxSets) { current = 0; el.classList.remove('done'); }
        else if (current === maxSets) { el.classList.add('done'); }
        el.setAttribute('data-current', current);
        el.innerText = `${current} / ${maxSets} Séries`;
        
        if (current === maxSets) {
            const item = el.closest('.exercise-item');
            const cb = item.querySelector('input[type="checkbox"]');
            if(!cb.checked) { cb.checked = true; item.classList.add('completed'); updateProgressBar(item.closest('.workout-card').id); }
        }
    }

    function openSwapModal(slotId, event) {
        event.stopPropagation();
        currentSwapSlotId = slotId;
        const cat = SLOT_CATEGORY[slotId] || "core_full"; 
        const listEl = document.getElementById('modalList');
        document.getElementById('modalTitle').innerText = "🔄 Selecione a Substituição";
        listEl.innerHTML = '';
        
        EXERCISE_DB[cat].forEach(ex => {
            listEl.innerHTML += `<button class="modal-btn" onclick="applySwap('${ex.nome}', ${ex.series}, '${ex.reps}', '${ex.yt}')">
                <strong>${ex.nome}</strong> ${ex.series} Séries | ${ex.reps}
            </button>`;
        });
        
        document.getElementById('swapModal').classList.add('active');
    }

    function closeSwapModal() { document.getElementById('swapModal').classList.remove('active'); currentSwapSlotId = null; }

    function applySwap(nome, series, reps, yt) {
        closeSwapModal();
        const payload = JSON.stringify({ tipo: "troca", nome, series, reps, yt });
        savePreferenceToDB(currentSwapSlotId, payload);
        renderSwap(currentSwapSlotId, { nome, series, reps, yt });
    }

    function renderSwap(slotId, ex) {
        const el = document.getElementById(slotId);
        if(!el) return;
        el.querySelector('.exercise-name').innerHTML = `${ex.nome} <button class="swap-btn" onclick="openSwapModal('${slotId}', event)">🔄 Trocar</button>`;
        const tags = el.querySelectorAll('.tag');
        tags[0].outerHTML = `<span class="tag set-counter" data-current="0" onclick="incrementSet(this, ${ex.series}, event)">0 / ${ex.series} Séries</span>`;
        tags[1].innerText = ex.reps;
        el.querySelector('.video-btn').href = `https://www.youtube.com/results?search_query=${ex.yt}`;
    }

    function savePreferenceToDB(slotId, jsonStr) {
        fetch(`${DB_URL}/preferencias_exercicios`, {
            method: "POST", headers: UPSERT_HEADERS, body: JSON.stringify({ slot_id: slotId, exercicio_selecionado: jsonStr })
        });
    }

    function loadPreferences() {
        fetch(`${DB_URL}/preferencias_exercicios?select=*`, { headers: HEADERS }).then(res => res.json()).then(data => {
            if(!Array.isArray(data)) return;
            data.forEach(pref => {
                try {
                    const ex = JSON.parse(pref.exercicio_selecionado);
                    if (ex.tipo === "troca") renderSwap(pref.slot_id, ex);
                    else if (ex.tipo === "novo") renderNewExercise(pref.slot_id, ex);
                } catch(e) {}
            });
        });
    }

    function openAddModal(dayId) {
        const listEl = document.getElementById('modalList');
        document.getElementById('modalTitle').innerText = "➕ Adicionar Novo Exercício";
        listEl.innerHTML = `<div class="recipe-form" style="margin:0; box-shadow:none;">
            <input type="text" id="newExName" placeholder="Nome do Exercício">
            <input type="number" id="newExSets" placeholder="Séries (ex: 3)">
            <input type="text" id="newExReps" placeholder="Repetições (ex: 12 Reps)">
            <button class="save-btn" style="padding: 10px; font-size: 1em;" onclick="submitNewExercise('${dayId}')">Confirmar Inclusão</button>
        </div>`;
        document.getElementById('swapModal').classList.add('active');
    }

    function submitNewExercise(dayId) {
        const nome = document.getElementById('newExName').value.trim();
        const series = parseInt(document.getElementById('newExSets').value);
        const reps = document.getElementById('newExReps').value.trim();
        if(!nome || !series || !reps) return alert("Preencha tudo!");
        
        const slotId = 'custom_' + Date.now();
        const yt = nome.replace(/ /g, '+');
        const ex = { tipo: "novo", dia: dayId, nome, series, reps, yt };
        
        savePreferenceToDB(slotId, JSON.stringify(ex));
        renderNewExercise(slotId, ex);
        closeSwapModal();
    }

    function renderNewExercise(slotId, ex) {
        const listEl = document.querySelector(`#${ex.dia} .exercise-list`);
        if(!listEl) return;
        const html = `<li class="exercise-item" id="${slotId}" onclick="toggleExercise('${slotId}', event)">
            <div class="checkbox-container"><input type="checkbox"></div>
            <div class="exercise-details">
                <div class="exercise-name">${ex.nome} <button class="swap-btn" style="color:var(--danger);" onclick="if(confirm('Remover?')) removeCustom('${slotId}', event)">🗑️ Remover</button></div>
                <div class="exercise-meta">
                    <span class="tag set-counter" data-current="0" onclick="incrementSet(this, ${ex.series}, event)">0 / ${ex.series} Séries</span><span class="tag">${ex.reps}</span>
                    <div class="weight-control"><input type="number" id="carga_${slotId}" placeholder="--" onclick="event.stopPropagation()"><span>kg</span><button class="save-weight-btn" onclick="saveWeight('${slotId}', event)">Salvar</button></div>
                </div>
            </div>
            <a href="https://www.youtube.com/results?search_query=${ex.yt}" target="_blank" class="video-btn">▶ Vídeo</a>
        </li>`;
        listEl.insertAdjacentHTML('beforeend', html);
        updateProgressBar(ex.dia);
    }

    function removeCustom(slotId, event) {
        event.stopPropagation();
        document.getElementById(slotId).remove();
        fetch(`${DB_URL}/preferencias_exercicios?slot_id=eq.${slotId}`, { method: "DELETE", headers: HEADERS });
    }

    // Call loadPreferences on page load (we can patch fetchTrainedDays to call it, or just put it at the end of the script)
    setTimeout(loadPreferences, 500);

"""
content = content.replace("    // --- TEMPORIZADOR LÓGICA ---", js_to_add + "\n    // --- TEMPORIZADOR LÓGICA ---")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("File updated successfully.")
