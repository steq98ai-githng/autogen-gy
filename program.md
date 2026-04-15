# AutoGen x JULES 每日演化排程
1. **目標**：利用 AutoGen 的多代理人對話機制，自動發現並修復專案中的技術債。
2. **執行動作**：每日透過 `python autogen_optimizer.py` 觸發 Critic 與 Executor 的對話。
3. **驗收標準**：若 Executor 成功執行了優化代碼且未報錯，JULES 應將變更提交為 Pull Request。
