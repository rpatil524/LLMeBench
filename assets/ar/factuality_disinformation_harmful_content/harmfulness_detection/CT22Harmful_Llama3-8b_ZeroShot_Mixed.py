import random

from llmebench.datasets import CT22HarmfulDataset
from llmebench.models import AzureModel
from llmebench.tasks import HarmfulDetectionTask


def metadata():
    return {
        "author": "Mohamed Bayan Kmainasi, Rakif Khan, Ali Ezzat Shahroor, Boushra Bendou, Maram Hasanain, and Firoj Alam",
        "affiliation": "Arabic Language Technologies, Qatar Computing Research Institute (QCRI), Hamad Bin Khalifa University (HBKU)",
        "model": "Llama-3.1-8B-Instruct",
        "description": "For a comprehensive analysis and results, refer to our peer-reviewed publication available at [Springer](https://doi.org/10.1007/978-981-96-0576-7_30) or explore the preprint version on [arXiv](https://arxiv.org/abs/2409.07054).",
    }


def config():
    return {
        "dataset": CT22HarmfulDataset,
        "task": HarmfulDetectionTask,
        "model": AzureModel,
        "model_args": {
            "class_labels": ["0", "1"],
            "max_tries": 30,
        },
        "general_args": {"test_split": "ar"},
    }


def prompt(input_sample):
    return [
        {
            "role": "user",
            "content": (
                "صنف التغريدة التالية على أنها 'harmful' أو 'not_harmful'. قدم التصنيف فقط.\n\n"
                + "تغريدة: "
                + input_sample
                + "التصنيف: "
            ),
        }
    ]


def post_process(response):
    # Extract the label from the response
    if "output" in response:
        label = response["output"].strip().lower()

    print("label: ", label)
    if "لا أستطيع تقديم هذا النوع من الإجابات." in label:
        return None
    elif "غير" in label or "ليس" in label or "not" in label:
        return "0"
    else:
        return "1"
