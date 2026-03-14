# penetration/adversary.py
# Human3D-FullLoop - Adversarial Attack Simulator (Non-commercial Research Only)
# ⚠️ This module is for LOCAL MODEL ROBUSTNESS TESTING ONLY.
# ⚠️ DO NOT use against third-party services or production systems.

import torch
import torch.nn as nn

class FGSMAttacker:
    """
    Fast Gradient Sign Method (FGSM) 攻击模拟器
    用于测试本地 3D 人体姿态/形状估计模型的鲁棒性
    """
    
    def __init__(self, epsilon=0.05):
        """
        Args:
            epsilon (float): 扰动强度（建议 0.01 ~ 0.1）
        """
        self.epsilon = epsilon

    def generate(self, model, x, y_true, loss_fn=None):
        """
        生成对抗样本（模拟）
        
        Args:
            model: 本地 PyTorch 模型（需支持 .eval() 和梯度）
            x: 输入张量（如 [batch, joints, 3] 关节点坐标）
            y_true: 真实标签（如 SMPL 参数）
            loss_fn: 损失函数（默认使用 MSE）
        
        Returns:
            x_adv: 对抗样本（与 x 同 shape）
        """
        if loss_fn is None:
            loss_fn = nn.MSELoss()
        
        x = x.clone().detach().requires_grad_(True)
        model.eval()
        
        with torch.enable_grad():
            output = model(x)
            loss = loss_fn(output, y_true)
            grad = torch.autograd.grad(loss, x, retain_graph=False)
        
        # FGSM 核心：sign(gradient) * epsilon
        perturbation = self.epsilon * grad.sign()
        x_adv = x + perturbation
        
        return x_adv.detach()

def demo_adversary():
    """演示函数（无实际模型，仅展示接口）"""
    print("[⚔️ 渗透·对抗者] 模拟对抗攻击流程...")
    print("→ 目标：本地 3D 人体重建模型")
    print("→ 方法：FGSM (epsilon=0.05)")
    print("→ 输出：扰动后的关节点输入")
    print("\n⚠️ 注意：此模块仅用于学术鲁棒性研究，禁止非法使用。")

if __name__ == "__main__":
    demo_adversary()