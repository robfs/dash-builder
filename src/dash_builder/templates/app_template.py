class AppTemplate:
    @staticmethod
    def content() -> str:
        return """
        import dash


        app = dash.Dash()

        if __name__ == "__main__":
            app.run(debug=True)
        """
