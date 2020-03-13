async def test_log_with_authors(git_repo_config, vcs):
    await vcs.clone()
    await vcs.update()
    revisions = await vcs.log()
    revisions = await vcs.log(author="Another Committer")
    revisions = await vcs.log(author="ac@d.not.zm.exist")
    revisions = await vcs.log(branch=vcs.get_default_revision(), author="Foo")
async def test_log_throws_errors_when_needed(vcs):
        await vcs.log(parent="HEAD", branch="master")
async def test_log_with_branches(git_repo_config, vcs):
    await vcs.clone()
    await vcs.update()
    revisions = await vcs.log(branch="B3")
    assert_revision(revisions[0], message="3rd branch")
    assert_revision(revisions[2], message="test")
    revisions = await vcs.log(branch=vcs.get_default_revision())
async def test_simple(vcs):
    await vcs.clone()
    await vcs.update()
    revision = (await vcs.log(parent="HEAD", limit=1))[0]
    revisions = await vcs.log()
    diff = await vcs.export(revisions[0].sha)
    revisions = await vcs.log(offset=0, limit=1)
    revisions = await vcs.log(offset=1, limit=1)
async def test_get_known_branches(git_repo_config, vcs):
    await vcs.clone()
    await vcs.update()
    branches = await vcs.get_known_branches()
    await vcs.update()
    branches = await vcs.get_known_branches()
async def test_show(git_repo_config, vcs):
    await vcs.clone()
    await vcs.update()
    revisions = await vcs.log()
    result = await vcs.show(revisions[0].sha, "BAZ")