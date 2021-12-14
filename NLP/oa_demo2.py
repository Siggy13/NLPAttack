'''
This example code shows how to  how to use the PWWS attack model to attack BERT on the SST-2 dataset.
'''
import OpenAttack
import datasets

def dataset_mapping(x):
    return {
        "x": x["sentence"],
        "y": 1 if x["label"] > 0.5 else 0,
    }
    
    
def main():
    victim = OpenAttack.loadVictim("BERT.SST")
    # BERT.SST is a pytorch model which is fine-tuned on SST-2. It uses Glove vectors for word representation.
    # The load operation returns a PytorchClassifier that can be further used for Attacker and AttackEval.

    dataset = datasets.load_dataset("sst", split="train[:1]").map(function=dataset_mapping)
    # We load the sst-2 dataset using `datasets` package, and map the fields.

    attacker = OpenAttack.attackers.BERTAttacker()
    # After this step, we’ve initialized a PWWSAttacker and uses the default configuration during attack process.

    attack_eval = OpenAttack.AttackEval(attacker, victim)
    # Use the default implementation for AttackEval which supports seven basic metrics.

    # eval_dict = attack_eval.eval(dataset, visualize=False)
    # print(eval_dict)
    simple_dataset = datasets.Dataset.from_dict({
    "x": [
        "I hate this movie.",
        "I like this apple."
    ],
    "y": [
        0, # 0 for negative
        1, # 1 for positive
    ]
})
    ieval = attack_eval.ieval(simple_dataset)
    for input in ieval:
        print(input)
    # Using visualize=True in attack_eval.eval can make it displays a visualized result. This function is really useful for analyzing small datasets.

if __name__ == "__main__":
    main()