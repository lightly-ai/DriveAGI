import argparse
import sys
import os
import re
import json
from pathlib import Path

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from utils.easydict import EasyDict

import lightspeed

pattern = r'batch_(\d+)-(\d+)'


def sort_by(dir: str):
    m = re.match(pattern, dir)
    if m:
        n1, n2 = m.groups()
        return int(n2)
    return 0


def select_images(config, ids):
    configs = EasyDict(json.load(open(config, "r")))
    root = {
        "train": configs.train_img_root,
        "val": configs.val_img_root
    }

    # Get right workspace for datapool
    workspaces = sorted(Path("workspaces").glob(f"batch_*"), key=lambda x: sort_by(x.name))
    if len(workspaces) > 0:
        import_workspace = workspaces[-1]
    else:
        import_workspace = Path("lotwheels1")

    ls = lightspeed.new(workspace=Path("workspaces") / f"batch_{ids[0]}-{ids[-1]}")
    ls.set_image_input_dir(input_dir=Path(root["train"]), glob="*/*/*.jpg")
    ls.prepare()
    ls.import_selection(import_workspace=import_workspace, selection_id="diverse")
    ls.select(
        selection_id="diverse",
        # 10 frames per second -> select 1 frame per second
        selection_config=lightspeed.selection_config.diverse(p=0.1),
    )
    ls.export_selection(
        output_file=Path("outputs") / "final.json",
        selection_id="diverse"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert OpenDV-YouTube meta data from csv to json')
    parser.add_argument('--config', type=str, default='configs/video2img.json')
    parser.add_argument('--video_ids', '-v', nargs='+', type=int, default=None, help='video ids to be processed')
    args = parser.parse_args()

    select_images(args.config, args.video_ids)