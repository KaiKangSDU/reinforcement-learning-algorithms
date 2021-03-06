import numpy as np
from arguments import get_args
from baselines.common.atari_wrappers import make_atari
from baselines.common.atari_wrappers import wrap_deepmind
from models import Net
import torch

def get_tensors(obs):
    obs = np.transpose(obs, (2, 0, 1))
    obs = np.expand_dims(obs, 0)
    obs = torch.tensor(obs, dtype=torch.float32)
    return obs

if __name__ == '__main__':
    args = get_args()
    # create the environment
    env = make_atari(args.env_name)
    env = wrap_deepmind(env, frame_stack=True)
    # create the network
    net = Net(env.action_space.n) 
    # model path
    model_path = args.save_dir + args.env_name + '/model.pt'
    # load the models
    net.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage))
    # start to test the demo
    obs = env.reset()
    for _ in range(2000):
        env.render()
        with torch.no_grad():
            obs_tensor = get_tensors(obs)
            action_value = net(obs_tensor)
        action = torch.argmax(action_value.squeeze()).item()
        obs, reward, done, _ = env.step(action)
        if done:
            obs = env.reset()
    env.close()
