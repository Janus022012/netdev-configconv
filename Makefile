make dev-test:
	python main.py create_config -cs ./data/input/config_sample/wa_config.log -ps ./data/input/parameter_sheets/WA1512パラメータシート.xlsx -rf ./data/input/rule/wa_rule.yml -op ./data/output/config/ -es 改版履歴

make build:
	pwd