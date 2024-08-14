import gradio as gr
from gradio_pdf import PDF
from PIL import Image
import os 
import json
import torch
from main import ArgumentParser, visualize_main

torch.set_grad_enabled(False)

with open('key_template/bol.txt', 'r') as f:
    bol_template = f.read()
with open('key_template/cv.txt', 'r') as f:
    cv_template = f.read() 
with open('key_template/identity_card.txt', 'r') as f:
    id_template = f.read()
with open('key_template/invoice.txt', 'r') as f:
    invoice_template = f.read()
with open('key_template/receipt.txt', 'r') as f:
    receipt_template = f.read()
with open('key_template/tax_form.txt', 'r') as f:
    taxform_template = f.read()


def run(file_path, key_template, output_dir, save_json_path, use_ocr, use_visualize, use_latin):
    with open('template.txt', 'w', encoding='utf-8') as f:
        f.write(key_template)
        keys = 'template.txt'

    args = ArgumentParser()
    args.file_path = file_path
    args.output_dir_path = output_dir
    args.keys = keys
    args.save_json_path = save_json_path
    args.use_ocr = use_ocr
    args.use_visualize = use_visualize
    args.use_latin = use_latin

    _, imgs = visualize_main(args)

    imgs_list = [Image.fromarray(img) for img in imgs]
    if len(imgs_list) > 1:
        imgs_list[0].save('running/convert.pdf', save_all=True, append_images=imgs_list[1:])
    else:
        imgs_list[0].save('running/convert.pdf', save_all=True)
    
    f = open(args.save_json_path)
    data = json.load(f)

    return 'running/convert.pdf', data


with gr.Blocks() as demo:
    gr.Markdown("""<p align="center"><strong><span style="font-size:2em;">Document Image Information Extraction</span></strong></p>""")
    with gr.Row():
        with gr.Column():
            file_path = gr.File(label='Document Input File Path')
            pdf = PDF(label='Output PDF', interactive=True)
            #output_file_path = gr.File(label='Output PDF File')
        
            with gr.Accordion("Options"):
                output_dir = gr.Textbox(label="Output Document Dir", value="output")
                save_json_path = gr.Textbox(label="JSON Output Path", value="running/output.json")
                use_ocr = gr.Checkbox(label="Use OCR", value=True)
                use_visualize = gr.Checkbox(label="Visualize", value=True)
                use_latin = gr.Checkbox(label="Use LATIN Prompt", value=False)
        
        with gr.Column():
            key_template = gr.Textbox(label="Key Template", placeholder = "Enter your desired key template")
            json_output = gr.JSON(label="JSON Output")
    
    examples = gr.Examples(examples=[['test_imgs/test_receipt.jpg', receipt_template]], inputs=[file_path, key_template])
    btn = gr.Button("Run")
    btn.click(fn = run, inputs=[file_path, key_template, output_dir, save_json_path, use_ocr, use_visualize, use_latin], outputs = [pdf, json_output])


if __name__ == "__main__":
    demo.launch(share=True)