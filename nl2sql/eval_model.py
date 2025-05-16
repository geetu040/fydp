import os

visible_devices = "0,1" # visible devices for vLLM
tensor_parallel_size = len(visible_devices.split(","))

model = "geetu040/tuned_sql_model"
model_name = model.split("/")[-1].strip()

dev_bird_eval_name = f"{model_name}_dev_bird"
dev_bird_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source bird --visible_devices {visible_devices} --input_file ./data/dev_bird.json --eval_name {dev_bird_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/bird/dev_20240627/dev.json --db_path ./data/bird/dev_20240627/dev_databases"
os.system(dev_bird_evaluation_cmd)

test_spider_eval_name = f"{model_name}_test_spider"
test_spider_evaluation_cmd = f"python3 auto_evaluation.py --output_ckpt_dir {model} --source spider --visible_devices {visible_devices} --input_file ./data/test_spider.json --eval_name {test_spider_eval_name} --tensor_parallel_size {tensor_parallel_size} --n 8 --gold_file ./data/spider/test_gold.sql --db_path ./data/spider/test_database"
os.system(test_spider_evaluation_cmd)
