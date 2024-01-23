import "./widget.css";

export function render({ model, el }) {
	let btn = document.createElement("button");
	btn.classList.add("ipyniivue_experimental-counter-button");
	btn.innerHTML = `count is ${model.get("value")}`;
	btn.addEventListener("click", () => {
		model.set("value", model.get("value") + 1);
		model.save_changes();
	});
	model.on("change:value", () => {
		btn.innerHTML = `count is ${model.get("value")}`;
	});
	el.appendChild(btn);
}
