from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    results = []
    if request.method == 'POST':
        items = request.form.getlist('item')
        probabilities = request.form.getlist('probability')
        try:
            # Convert probabilities to float with up to 6 decimal places
            probabilities = [round(float(p), 6) for p in probabilities]
        except ValueError:
            message = '확률은 숫자여야 합니다.'
            return render_template('index.html', items=zip(items, probabilities), message=message)

        total = sum(probabilities)
        if total != 100.0:
            difference = round(total - 100.0, 6)
            if difference > 0:
                message = f'확률의 합이 100%를 초과했습니다: {difference}%'
            else:
                message = f'확률의 합이 100% 미만입니다: {abs(difference)}%'
            return render_template('index.html', items=zip(items, probabilities), message=message)

        # Create a list of items with their cumulative probabilities
        cumulative_prob = []
        cumulative = 0.0
        for item, prob in zip(items, probabilities):
            cumulative += prob
            cumulative_prob.append((item, cumulative))

        if 'draw' in request.form:
            # Single draw
            rand = random.uniform(0, 100)
            for item, cum_prob in cumulative_prob:
                if rand <= cum_prob:
                    results.append(item)
                    break
        elif 'continuous_draw' in request.form:
            # Continuous draw
            try:
                count = int(request.form.get('count', 1))
                if count < 1:
                    message = '연속 추첨 횟수는 1 이상이어야 합니다.'
                    return render_template('index.html', items=zip(items, probabilities), message=message)
            except ValueError:
                message = '연속 추첨 횟수는 정수여야 합니다.'
                return render_template('index.html', items=zip(items, probabilities), message=message)
            
            for _ in range(count):
                rand = random.uniform(0, 100)
                for item, cum_prob in cumulative_prob:
                    if rand <= cum_prob:
                        results.append(item)
                        break

    else:
        # Initialize with 2 empty items
        items = ['', '']
        probabilities = ['', '']

    return render_template('index.html', items=zip(items, probabilities), message=message, results=results)

if __name__ == '__main__':
    app.run(debug=True)
