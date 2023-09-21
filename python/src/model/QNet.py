import torch.nn as nn


class QNet(nn.Module):
    def __init__(self, hidden_layer=512, normalize_image=True) -> None:
        super(QNet, self).__init__()

        number_of_outputs = 3
        self.normalize_image = normalize_image

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)

        self.advantage1 = nn.Linear(7 * 7 * 64, hidden_layer)
        self.advantage2 = nn.Linear(hidden_layer, number_of_outputs)

        self.value1 = nn.Linear(7 * 7 * 64, hidden_layer)
        self.value2 = nn.Linear(hidden_layer, 1)

        # self.activation = nn.Tanh()
        self.activation = nn.ReLU()

    def forward(self, x):
        if self.normalize_image:
            x = x / 255

        output_conv = self.conv1(x)
        output_conv = self.activation(output_conv)

        output_conv = self.conv2(output_conv)
        output_conv = self.activation(output_conv)
        output_conv = self.conv3(output_conv)
        output_conv = self.activation(output_conv)

        output_conv = output_conv.view(output_conv.size(0), -1)  # flatten

        output_advantage = self.advantage1(output_conv)
        output_advantage = self.activation(output_advantage)
        output_advantage = self.advantage2(output_advantage)

        output_value = self.value1(output_conv)
        output_value = self.activation(output_value)
        output_value = self.value2(output_value)

        output_final = output_value + output_advantage - output_advantage.mean()

        return output_final