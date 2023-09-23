import torch
import torch.nn as nn


# UNet
class UNet(nn.Module):
    def __init__(self, input_channels, output_channels):
        super().__init__()
        self.conv1 = conv_bn_relu(input_channels, 16)
        self.conv2 = conv_bn_relu(16, 32)
        self.conv3 = conv_bn_relu(32, 64)
        self.conv4 = conv_bn_relu(64, 128)
        self.conv5 = conv_bn_relu(128, 256)
        self.down_pooling = nn.MaxPool2d(2)

        self.up_pool6 = up_pooling(256, 128)
        self.conv6 = conv_bn_relu(256, 128)
        self.up_pool7 = up_pooling(128, 64)
        self.conv7 = conv_bn_relu(128, 64)
        self.up_pool8 = up_pooling(64, 32)
        self.conv8 = conv_bn_relu(64, 32)
        self.up_pool9 = up_pooling(32, 16)
        self.conv9 = conv_bn_relu(32, 16)
        self.conv10 = nn.Conv2d(16, output_channels, 1)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight.data, a=0, mode="fan_out")
                if m.bias is not None:
                    m.bias.data.zero_()

    def forward(self, x):
        x1 = self.conv1(x)
        p1 = self.down_pooling(x1)
        x2 = self.conv2(p1)
        p2 = self.down_pooling(x2)
        x3 = self.conv3(p2)
        p3 = self.down_pooling(x3)
        x4 = self.conv4(p3)
        p4 = self.down_pooling(x4)
        x5 = self.conv5(p4)

        p6 = self.up_pool6(x5)
        x6 = torch.cat([p6, x4], dim=1)
        x6 = self.conv6(x6)

        p7 = self.up_pool7(x6)
        x7 = torch.cat([p7, x3], dim=1)
        x7 = self.conv7(x7)

        p8 = self.up_pool8(x7)
        x8 = torch.cat([p8, x2], dim=1)
        x8 = self.conv8(x8)

        p9 = self.up_pool9(x8)
        x9 = torch.cat([p9, x1], dim=1)
        x9 = self.conv9(x9)

        output = self.conv10(x9)
        output = torch.sigmoid(output)

        return output


def conv_bn_relu(in_channels, out_channels, kernel_size=3, stride=1, padding=1):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True),
        nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True),
    )


def down_pooling():
    return nn.MaxPool2d(2)


def up_pooling(in_channels, out_channels, kernel_size=2, stride=2):
    return nn.Sequential(
        # 転置畳み込み
        nn.ConvTranspose2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True),
    )


# unet = UNet(3, 3)

# tensor = torch.rand(5, 3, 112, 112)

# print(tensor.shape, "input")
# x1 = self.conv1(x)
# p1 = self.down_pooling(x1)
# x2 = self.conv2(p1)
# p2 = self.down_pooling(x2)
# x3 = self.conv3(p2)
# p3 = self.down_pooling(x3)
# x4 = self.conv4(p3)
# p4 = self.down_pooling(x4)
# x5 = self.conv5(p4)

# p6 = self.up_pool6(x5)
# x6 = torch.cat([p6, x4], dim=1)
# x6 = self.conv6(x6)

# p7 = self.up_pool7(x6)
# x7 = torch.cat([p7, x3], dim=1)
# x7 = self.conv7(x7)

# p8 = self.up_pool8(x7)
# x8 = torch.cat([p8, x2], dim=1)
# x8 = self.conv8(x8)

# p9 = self.up_pool9(x8)
# x9 = torch.cat([p9, x1], dim=1)
# x9 = self.conv9(x9)

# output = self.conv10(x9)
# output = torch.sigmoid(output)

# x1 = unet.conv1(tensor)
# print(x1.shape, "x1")
# p1 = unet.down_pooling(x1)
# print(p1.shape, "p1")
# x2 = unet.conv2(p1)
# print(x2.shape, "x2")
# p2 = unet.down_pooling(x2)
# print(p2.shape, "p2")
# x3 = unet.conv3(p2)
# print(x3.shape, "x3")
# p3 = unet.down_pooling(x3)
# print(p3.shape, "p3")
# x4 = unet.conv4(p3)
# print(x4.shape, "x4")
# p4 = unet.down_pooling(x4)
# print(p4.shape, "p4")
# x5 = unet.conv5(p4)
# print(x5.shape, "x5")

# p6 = unet.up_pool6(x5)
# print(p6.shape, "p6")
# x6 = torch.cat([p6, x4], dim=1)
# print(x6.shape, "x6")
# x6 = unet.conv6(x6)
# print(x6.shape, "x6")

# p7 = unet.up_pool7(x6)
# print(p7.shape, "p7")
# x7 = torch.cat([p7, x3], dim=1)
# print(x7.shape, "x7")
# x7 = unet.conv7(x7)
# print(x7.shape, "x7")

# p8 = unet.up_pool8(x7)
# print(p8.shape, "p8")
# x8 = torch.cat([p8, x2], dim=1)
# print(x8.shape, "x8")
# x8 = unet.conv8(x8)
# print(x8.shape, "x8")

# p9 = unet.up_pool9(x8)
# print(p9.shape, "p9")
# x9 = torch.cat([p9, x1], dim=1)
# print(x9.shape, "x9")
# x9 = unet.conv9(x9)
# print(x9.shape, "x9")

# output = unet.conv10(x9)
# print(output.shape, "output")
# output = torch.sigmoid(output)
# print(output.shape, "output")

# torch.Size([5, 3, 300, 300]) input
# torch.Size([5, 16, 300, 300]) x1
# torch.Size([5, 16, 150, 150]) p1
# torch.Size([5, 32, 150, 150]) x2
# torch.Size([5, 32, 75, 75]) p2
# torch.Size([5, 64, 75, 75]) x3
# torch.Size([5, 64, 37, 37]) p3
# torch.Size([5, 128, 37, 37]) x4
# torch.Size([5, 128, 18, 18]) p4
# torch.Size([5, 256, 18, 18]) x5
# torch.Size([5, 128, 37, 37]) p6
# torch.Size([5, 256, 37, 37]) x6
# torch.Size([5, 64, 75, 75]) p7
# torch.Size([5, 128, 75, 75]) x7
# torch.Size([5, 32, 150, 150]) p8
# torch.Size([5, 64, 150, 150]) x8
# torch.Size([5, 16, 300, 300]) p9
# torch.Size([5, 32, 300, 300]) x9
# torch.Size([5, 3, 300, 300]) output
# torch.Size([5, 3, 300, 300]) output
