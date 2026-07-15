import pytest

from unisafe.resources import prompt_template, taxonomy


@pytest.mark.parametrize("task", ["TI", "IE", "IC", "MT", "TT", "IT", "MU"])
def test_every_task_has_a_prompt(task):
    prompt = prompt_template(task)
    assert "{taxonomy_section}" in prompt
    rendered = prompt.format(
        taxonomy_section="taxonomy",
        output_image_desc="target",
        instruction="instruction",
        input_text="input",
        output_text="output",
        instruction_t1="one",
        instruction_t2="two",
        instruction_t3="three",
        instruction_t4="four",
    )
    assert "taxonomy" in rendered


def test_taxonomy_sizes():
    image = taxonomy("TI")
    text = taxonomy("TT")
    assert sum(len(category["subcategories"]) for category in image.values()) == 15
    assert sum(len(category["subcategories"]) for category in text.values()) == 21
