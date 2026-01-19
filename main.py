import sys
from services.comment_loader import CommentLoader
from domain.user import User
from config.env import EnvConfig

def main() -> int:
    env_config: EnvConfig = EnvConfig()
    comment_loader: CommentLoader = CommentLoader(env_config)
    user: User = comment_loader.load_all()

    print(user)
    user.print_account_comments()
    
    return 0

if __name__ == "__main__":
    result = main()
    print("INFO: Program ran successfully" if result == 0 else "INFO: Program crashed")
    sys.exit(result) 