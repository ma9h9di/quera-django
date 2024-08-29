from django.shortcuts import render


def custom_bad_request(request, exception=None):
    # Example of a custom error message based on logic
    error_message = "Sorry, there was an issue with your request."

    if exception:
        # Customize the message based on exception details if available
        error_message = f"Custom Error: {str(exception)}"

    return render(request, '400.html', {'error_message': error_message}, status=400)
