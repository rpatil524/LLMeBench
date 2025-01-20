from llmebench.datasets import SpamDataset
from llmebench.models import FastChatModel
from llmebench.tasks import SpamTask


def metadata():
    return {
        "author": "Mohamed Bayan Kmainasi, Rakif Khan, Ali Ezzat Shahroor, Boushra Bendou, Maram Hasanain, and Firoj Alam",
        "affiliation": "Arabic Language Technologies, Qatar Computing Research Institute (QCRI), Hamad Bin Khalifa University (HBKU)",
        "model": "jais-13b-chat",
        "description": "For a comprehensive analysis and results, refer to our peer-reviewed publication available at [Springer](https://doi.org/10.1007/978-981-96-0576-7_30) or explore the preprint version on [arXiv](https://arxiv.org/abs/2409.07054).",
    }


def config():
    return {
        "dataset": SpamDataset,
        "task": SpamTask,
        "model": FastChatModel,
        "model_args": {
            "class_labels": ["__label__ADS", "__label__NOTADS"],
            "max_tries": 3,
        },
    }


def few_shot_prompt(input_sample, base_prompt, examples):
    out_prompt = base_prompt + "\n\n"
    out_prompt += "إليك بعض الأمثلة:\n\n"
    for index, example in enumerate(examples):
        label = (
            "__label__ADS" if example["label"] == "__label__ADS" else "__label__NOTADS"
        )
        out_prompt += (
            f"مثال {index + 1}:\n"
            f"الجملة: '{example['input']}'\n"
            f"التصنيف: {label}\n\n"
        )

    # Append the sentence we want the model to predict for but leave the Label blank
    out_prompt += f"الجملة: '{input_sample}'\nالتصنيف: \n"

    return out_prompt


def prompt(input_sample, examples):
    base_prompt = "صنف الجملة التالية كـ '__label__ADS' أو '__label__NOTADS'، أعد التسمية فقط بدون الحاجة إلى وصف أو تحليل.\n"
    return [
        {
            "role": "user",
            "content": few_shot_prompt(input_sample, base_prompt, examples),
        }
    ]


def post_process(response):
    label = response["choices"][0]["message"]["content"].lower()

    label = label.replace("label:", "").strip()
    print("label", label)
    if "ليس" in label or "ليست" in label or "not" in label:
        return "__label__NOTADS"
    return "__label__ADS"
