import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunnerMP

from tictactoe import get_game_grid, TicTacToe


runner = BatchRunnerMP(
    TicTacToe,
    nr_processes=2,
    iterations=256,
    model_reporters={'endgame': lambda m: m.endgame, 'endgrid': get_game_grid},
)

runner.run_all()

df = runner.get_model_vars_dataframe()
print(df.endgame.value_counts())

fig = plt.figure(figsize=(16, 16))
for i in range(256):
    subplot = fig.add_subplot(16, 16, i + 1)
    subplot.imshow(df.endgrid[i])
    subplot.axis('off')
    subplot.set_title(df.endgame[i].name, size=8)

fig.tight_layout()
plt.subplots_adjust(wspace=-.9)
