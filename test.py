Building loop for X-Cycle

    Have:
        List of strong links that connect either to a strong or weak link
        List of weak links that connect on one end to a strong link and other end to strong or weak link

    Start with any strong link
        Look at all possible strong and weak link next links
        Depth first search for each choice
        if current is strong, next can be weak or strong
        if current is weak, if previous is weak then next must be strong, else can be weak or strong

    Each time a link is added, check cell at end of the link to see if it creates a loop to someplace in the current chain
    If a loop is found:
        Call separate routine that will:
            Categorize loop for Rule 1, 2 or 3
            Determine if any cells can be cleared
            Return true if a cell was cleared
        Can then stop processing and start big loop over again


